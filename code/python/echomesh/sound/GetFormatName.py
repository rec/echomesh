from __future__ import absolute_import, division, print_function, unicode_literals

import pyaudio

from echomesh.util import Log

LOGGER = Log.logger(__name__)

FORMAT_NAMES = {
  1: pyaudio.paInt8,
  2: pyaudio.paInt16,
  3: pyaudio.paInt24,
  4: pyaudio.paInt32,
  }

def get_format_name(sample_bytes):
  fmt = FORMAT_NAMES.get(sample_bytes, 0)
  if fmt:
    return fmt
  LOGGER.error("Didn't understand sample_bytes = %s.", sample_bytes)
  return FORMAT_NAMES[1]
