from __future__ import absolute_import, division, print_function, unicode_literals

import aifc
import math
import sunau
import wave

from echomesh.util import ImportIf
numpy = ImportIf.imp('numpy')

FILE_READERS = {'au': sunau, 'aifc': aifc, 'aiff': aifc, 'wav': wave}

def numpy_types():
  return {1: numpy.uint8, 2: numpy.int16, 4: numpy.int32}

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
