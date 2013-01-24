# from __future__ import absolute_import, division, print_function, unicode_literals

import aifc
import copy
import math
import numpy
import os.path
import sndhdr
import struct
import sunau
import wave

from echomesh.base import Config
from echomesh.sound import Sound
from echomesh.util.math import Envelope
from echomesh.util import Log
from echomesh.util.file import DefaultFile
from echomesh.util import Subprocess
from echomesh.util.thread.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

BITS_PER_BYTE = 8

# https://github.com/rec/echomesh/issues/115
DEFAULT_AUDIO_DIRECTORY = DefaultFile.DefaultFile('assets/audio')
OUTPUT_DEVICE_INDEX = Config.get('audio', 'output', 'device')
MAX_DEVICE_NUMBERS = 8

# Adapted from http://flamingoengine.googlecode.com/svn-history/r70/trunk/backends/audio/pyaudio_mixer.py

def interleave(left, right):
  """Convert two mono sources into one stereo source."""
  return numpy.ravel(numpy.vstack((left, right)), order='F')

def uninterleave(src):
  """Convert one stereo source into two mono sources."""
  return src.reshape(2, len(src)/2, order='FORTRAN')

def pan_to_angle(pan):
  return (pan + 1.0) * math.pi / 4.0

def calculate_pan(pan):
  """Pan two mono sources in the stereo field."""
  if pan < -1:
    pan = -1
  elif pan > 1:
    pan = 1

  angle = pan_to_angle(pan)
  return math.cos(angle), math.sin(angle)


class FilePlayer(ThreadLoop):
  HANDLERS = dict(au=sunau, aifc=aifc, aiff=aifc, wav=wave)
  DTYPES = {1: numpy.uint8, 2: numpy.int16, 4: numpy.int32}

  def __init__(self, file, level=1, pan=0, loops=1):
    super(FilePlayer, self).__init__(name='FilePlayer')

    self.debug = True
    self.passthrough = (level == 1 and pan == 0)

    self.level = Envelope.make_envelope(level)
    self.pan = Envelope.make_envelope(pan)
    self.loops = loops

    filename = DEFAULT_AUDIO_DIRECTORY.expand(file)
    filetype = sndhdr.what(filename)[0]
    handler = FilePlayer.HANDLERS.get(filetype, None)
    if not handler:
      LOGGER.error("Can't understand the file type of file %s", filename)
      self.close()
      return

    self.file_stream = handler.open(filename, 'rb')
    self.sample_width = self.file_stream.getsampwidth()

    (self.channels, self.sample_width, self.sampling_rate,
     nsamples, c1, c2) = self.file_stream.getparams()
    self.dtype = FilePlayer.DTYPES[self.sample_width]
    self.request_channels = 2 if self.pan else self.channels
    self.format = Sound.PYAUDIO.get_format_from_width(self.sample_width)
    self.samples_per_frame = self.sample_width * self.channels
    self.loop_number = 0
    self.restart_sound()

  def open_stream(self, index):
    try:
      frames_per_buffer = Config.get('audio', 'output', 'frames_per_buffer')
      return Sound.PYAUDIO.open(format=self.format,
                                channels=self.request_channels,
                                rate=self.sampling_rate,
                                output=True,
                                output_device_index=index,
                                frames_per_buffer=frames_per_buffer)
    except:
      pass

  def restart_sound(self):
    self._close_stream()
    global OUTPUT_DEVICE_INDEX
    if OUTPUT_DEVICE_INDEX is -1:
      for i in range(MAX_DEVICE_NUMBERS):
        self.audio_stream = self.open_stream(i)
        if self.audio_stream:
          LOGGER.info('Successfully opened output stream on index %d', i)
          OUTPUT_DEVICE_INDEX = i
          break
    else:
      self.audio_stream = self.open_stream(OUTPUT_DEVICE_INDEX)

    if not self.audio_stream:
      LOGGER.error("Couldn't reopen sound on loop %d", self.loop_number)
      self.close()
    self.time = 0
    self.current_level = self.level.interpolate(0)
    self.current_pan = self.pan.interpolate(0)

  def close(self):
    super(FilePlayer, self).close()
    self._close_stream()

  def _close_stream(self):
    if getattr(self, 'audio_stream', None):
      self.audio_stream.stop_stream()
      self.audio_stream.close()

  def _convert(self, frames):
    frames = numpy.fromstring(frames, dtype=self.dtype)
    if self.sample_width is 1:
      frames *= 256.0
    elif self.sample_width is 4:
      frames /= 65536.0

    if self.channels is 1:
      return numpy.vstack((frames, numpy.array(frames)))
    else:
      return uninterleave(frames)

  def run(self):
    chunk_size = Config.get('audio', 'output', 'chunk_size')
    frames = self.file_stream.readframes(chunk_size)
    if not frames:
      self.loop_number += 1
      if self.loop_number < self.loops:
        self.restart_sound()
        if not self.is_running:
          return
      else:
        self.close()
        return

    self.time =+ len(frames) / float((self.samples_per_frame *
                                      self.sampling_rate))

    frames = self._pan_and_fade(frames)
    try:
      self.audio_stream.write(frames)
    except:
      if self.is_running:
        raise

  def _pan_and_fade(self, frames):
    if self.passthrough:
      return frames
    left, right = self._convert(frames)
    if self.level.is_constant:
      left *= self.current_level
      right *= self.current_level
    else:
      next_level = self.level.interpolate(self.time)
      levels = numpy.linspace(self.current_level, next_level, len(left))
      left *= levels
      right *= levels
      self.current_level = next_level

    if self.pan.is_constant:
      lpan, rpan = calculate_pan(self.current_pan)
      left *= lpan
      right *= rpan
    else:
      next_pan = self.pan.interpolate(self.time)
      angles = numpy.linspace(pan_to_angle(self.current_pan),
                              pan_to_angle(next_pan), len(left))

      left *= numpy.cos(angles)
      right *= numpy.sin(angles)
      self.current_pan = next_pan

    return interleave(left, right).tostring()

def play_with_aplay(file, **kwds):
  file = DEFAULT_AUDIO_DIRECTORY.expand(file)
  result, returncode = Subprocess.run(['/usr/bin/aplay', file])
  if returncode:
    LOGGER.error('Unable to play file %s using aplay', file)

def play(**keywords):
  aplay = Config.get('audio', 'output', 'use_aplay')
  return (play_with_aplay if aplay else FilePlayer)(**keywords)
