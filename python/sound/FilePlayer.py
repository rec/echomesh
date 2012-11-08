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

from sound import Sound
from util import Envelope
from util.DefaultFile import DefaultFile
from util import ThreadLoop

DEFAULT_CHUNK_SIZE = 1024
BITS_PER_BYTE = 8

DEFAULT_AUDIO_DIRECTORY = DefaultFile('~/echomesh/assets/audio/')
OUTPUT_DEVICE_INDEX = -1
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
  if pan < -1: pan = -1
  elif pan > 1: pan = 1

  angle = pan_to_angle(pan)
  return math.cos(angle), math.sin(angle)


class FilePlayer(ThreadLoop.ThreadLoop):
  HANDLERS = dict(au=sunau, aifc=aifc, aiff=aifc, wav=wave)
  DTYPES = {1: numpy.uint8, 2: numpy.int16, 4: numpy.int32}

  def __init__(self, file, level=1.0, pan=0, loops=1,
               chunk_size=DEFAULT_CHUNK_SIZE):
    ThreadLoop.ThreadLoop.__init__(self)

    self.debug = True
    self.chunk_size = chunk_size
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
    self.restart_sound()

  def open_stream(self, index):
    try:
      return Sound.PYAUDIO.open(format=self.format,
                                channels=self.request_channels,
                                rate=self.sampling_rate,
                                output=True,
                                output_device_index=index)
    except:
      return None

  def restart_sound(self):
    global OUTPUT_DEVICE_INDEX
    if OUTPUT_DEVICE_INDEX is -1:
      for i in range(MAX_DEVICE_NUMBERS):
        self.audio_stream = self.open_stream(i)
        if self.audio_stream:
          OUTPUT_DEVICE_INDEX = i
          break
    else:
      self.audio_stream = self.open_stream(OUTPUT_DEVICE_INDEX)

    assert self.audio_stream
    self.time = 0
    self.current_level = self.level.interpolate(0)
    self.current_pan = self.pan.interpolate(0)
    self.loop_number = 0

  def close(self):
    ThreadLoop.ThreadLoop.close(self)
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
    frames = self.file_stream.readframes(self.chunk_size)
    if not frames:
      self.loop_number += 1
      if self.loop_number < self.loops:
        self.restart_sound()
      else:
        self.close()
        return

    new_time = self.time + float(len(frames)) / (self.samples_per_frame
                                                 * self.sampling_rate)

    left, right = self._convert(frames)
    if self.level.is_constant:
      left *= self.current_level
      right *= self.current_level
    else:
      next_level = self.level.interpolate(new_time)
      levels = numpy.linspace(self.current_level, next_level, len(left))
      left *= levels
      right *= levels
      self.current_level = next_level

    if self.pan.is_constant:
      lpan, rpan = calculate_pan(self.current_pan)
      left *= lpan
      right *= rpan
    else:
      next_pan = self.pan.interpolate(new_time)
      angles = numpy.linspace(pan_to_angle(self.current_pan),
                              pan_to_angle(next_pan), len(left))

      left *= numpy.cos(angles)
      right *= numpy.sin(angles)
      self.current_pan = next_pan

    frames = interleave(left, right).tostring()

    self.time = new_time
    self.audio_stream.write(frames)

