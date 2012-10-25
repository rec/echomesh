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
from util import ThreadLoop

# DEFAULT_CHUNK_SIZE = 1024
DEFAULT_CHUNK_SIZE = 8
BITS_PER_BYTE = 8
DEBUG = False

def _print_string(frames):
  if not DEBUG:
    return

  print('  *****')
  print('_print_string', len(frames), type(frames))
  for f in frames:
    print(ord(f))
  print('  *****')

def _print_frame(frames):
  if not DEBUG:
    return

  print('  *****')
  print('_print_frame', len(frames), type(frames))
  for f in frames:
    print(f)
  print('  *****')

# Adapted from http://flamingoengine.googlecode.com/svn-history/r70/trunk/backends/audio/pyaudio_mixer.py

def interleave(left, right):
    """Convert two mono sources into one stereo source."""
    return numpy.ravel(numpy.vstack((left, right)), order='F')

def uninterleave(src):
  """Convert one stereo source into two mono sources."""
  return src.reshape(2, len(src)/2, order='FORTRAN')

def calculate_pan(pan):
  """Pan two mono sources in the stereo field."""
  if pan < -1: pan = -1
  elif pan > 1: pan = 1

  pan = (pan + 1.0) * math.pi / 4.0
  return math.cos(pan), math.sin(pan)


class FilePlayer(ThreadLoop.ThreadLoop):
  HANDLERS = dict(au=sunau, aifc=aifc, aiff=aifc, wav=wave)
  DTYPES = {1: numpy.uint8, 2: numpy.int16, 4: numpy.int32}

  def __init__(self, filename, level=1.0, pan=0,
               chunk_size=DEFAULT_CHUNK_SIZE):
    ThreadLoop.ThreadLoop.__init__(self)

    self.debug = True
    self.chunk_size = chunk_size
    self.level = level
    self.pan = pan
    self.must_convert = (pan or type(level) == 'object' or level < 1.0)

    fname = os.path.expanduser(filename)
    filetype = sndhdr.what(fname)[0]
    self.file_stream = FilePlayer.HANDLERS[filetype].open(filename, 'rb')
    self.sample_width = self.file_stream.getsampwidth()
    format = Sound.PYAUDIO.get_format_from_width(self.sample_width)

    (self.channels, self.sample_width, self.sampling_rate,
     n, c1, c2) = self.file_stream.getparams()
    self.dtype = FilePlayer.DTYPES[self.sample_width]
    self.request_channels = 2 if self.pan else self.channels
    self.audio_stream = Sound.PYAUDIO.open(format=format,
                                           channels=self.request_channels,
                                           rate=self.sampling_rate,
                                           output=True)


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
    if frames:
      if self.must_convert:
        left, right = self._convert(frames)
        if type(self.level) == 'object':
          pass
        else:
          left *= self.level
          right *= self.level

        if type(self.pan) == 'object':
          pass
        else:
          lpan, rpan = calculate_pan(self.pan)
          left *= lpan
          right *= rpan

        frames = interleave(left, right).tostring()

      self.audio_stream.write(frames)
    else:
      self.close()

