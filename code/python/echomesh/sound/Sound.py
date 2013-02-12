from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Importer
pyaudio = Importer.imp('pyaudio')

_PYAUDIO = None

def PYAUDIO():
  global _PYAUDIO
  if not _PYAUDIO:
    _PYAUDIO = pyaudio.PyAudio()
  return _PYAUDIO

INPUT, OUTPUT = True, False

def devices():
  for i in range(PYAUDIO().get_device_count()):
    yield PYAUDIO().get_device_info_by_index(i)

def get_default_device(is_input):
  if is_input:
    return PYAUDIO().get_default_input_device_info()
  else:
    return PYAUDIO().get_default_output_device_info()

def get_default_index(is_input):
  return get_default_device(is_input)['index']

def get_index_from_name(is_input, name):
  name = name.lower()
  inout_field = 'maxInputChannels' if is_input else 'maxOutputChannels'
  for d in devices():
    if d['name'].lower().startswith(name) and d[inout_field]:
      return d['index']

  return -1

def get_index(is_input, get):
  inout = 'input' if is_input else 'output'
  name = get('audio', inout, 'name')
  index = get('audio', inout, 'index')
  if name:
    name_index = get_index_from_name(is_input, name)
    if name_index >= 0:
      return name_index
  if index >= 0:
    return index
  return get_default_index(is_input)

def get_input_index(get):
  return get_index(True, get)

def get_output_index(get):
  return get_index(False, get)

def get_device_info():
  return PYAUDIO().get_device_info_by_index()

LIST_FORMAT = ('{index}: {name:24}: {maxInputChannels} in, ' +
               '{maxOutputChannels} out at {defaultSampleRate}Hz')

def list_ports(print=print):
  for d in devices():
    print(LIST_FORMAT.format(**d))

