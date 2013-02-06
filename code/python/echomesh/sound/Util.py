from __future__ import absolute_import, division, print_function, unicode_literals

import aifc
import math
import numpy
import sunau
import wave

from echomesh.base import Config
from echomesh.base import Platform
from echomesh.util import Log
from echomesh.util import Subprocess
from echomesh.util.file import DefaultFile

LOGGER = Log.logger(__name__)

DEFAULT_AUDIO_DIRECTORY = DefaultFile.DefaultFile('asset/audio')

FILE_READERS = {'au': sunau, 'aifc': aifc, 'aiff': aifc, 'wav': wave}
NUMPY_TYPES = {1: numpy.uint8, 2: numpy.int16, 4: numpy.int32}

# Adapted from http://flamingoengine.googlecode.com/svn-history/r70/trunk/backends/audio/pyaudio_mixer.py

# TODO: config client

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

def play_with_aplay(file, **kwds):
  file = DEFAULT_AUDIO_DIRECTORY.expand(file)
  binary = Config.get('audio', 'input', 'aplay_binary')
  if not binary:
    if Platform.IS_LINUX:
      binary = '/usr/bin/aplay'
    elif Platform.IS_MAC:
      binary = '/usr/bin/afplay'

  if binary:
    result, returncode = Subprocess.run([binary, file])
    if returncode:
      LOGGER.error('Unable to play file %s using aplay', file)
  else:
    LOGGER.error("Couldn't locate binary for platform %s", Platform.PLATFORM)

