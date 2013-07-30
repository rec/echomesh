from __future__ import absolute_import, division, print_function, unicode_literals

import aifc
import math
import sunau
import wave

from echomesh.util import ImportIf
from echomesh.util.file import DefaultFile

numpy = ImportIf.imp('numpy')

FILE_READERS = {'au': sunau, 'aifc': aifc, 'aiff': aifc, 'wav': wave}

DEFAULT_AUDIO_DIRECTORY = DefaultFile.DefaultFile('asset/audio')

def numpy_types():
  return {1: numpy.uint8, 2: numpy.int16, 4: numpy.int32}

# Adapted from http://flamingoengine.googlecode.com/svn-history/r70/trunk/backends/audio/pyaudio_mixer.py

def interleave(left, right):
  """Convert two mono sources into one stereo source."""
  return numpy.ravel(numpy.vstack((left, right)), order='F')

def uninterleave(src):
  """Convert one stereo source into two mono sources."""
  return src.reshape(2, len(src) / 2, order='FORTRAN')

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

def to_numpy(frames, dtype, sample_width, channels):
  frames = numpy.fromstring(frames, dtype=dtype)
  if sample_width == 1:
    frames *= 256.0
  elif sample_width == 4:
    frames /= 65536.0

  if channels == 1:
    return numpy.vstack((frames, numpy.array(frames)))
  else:
    return Util.uninterleave(frames)
