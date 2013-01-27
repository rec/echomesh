from __future__ import absolute_import, division, print_function, unicode_literals

import pyaudio

PYAUDIO = pyaudio.PyAudio()

def get_index(is_input, name=None):
  if not name:
    if is_input:
      info = PYAUD.get_default_input_device_info()
    else:
      info = PYAUD.get_default_output_device_info()
    return info['index']

  inout_field = 'maxInputChannels' if is_input else 'maxOutputChannels'
  for i in range(PYAUDIO.get_device_count()):
    info = PYAUDIO.get_device_info_by_index(i)
    if info['name'].startswith(name) and info[inout_field]:
      return i

  return -1


def stop():
  PYAUDIO.terminate()
