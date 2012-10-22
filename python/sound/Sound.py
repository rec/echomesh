from __future__ import absolute_import, division, print_function, unicode_literals

import pyaudio

PYAUDIO = pyaudio.PyAudio()

def close():
  PYAUDIO.terminate()
