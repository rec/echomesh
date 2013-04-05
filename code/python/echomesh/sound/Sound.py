from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import ImportIf
pyaudio = ImportIf.imp('pyaudio')

_PYAUDIO = None

_LIST_FORMAT = ('{name:24}: {maxInputChannels} in, ' +
               '{maxOutputChannels} out at {defaultSampleRate}Hz')

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

def get_index_field_from_name(is_input, name, field):
  name = name.lower()
  for d in devices():
    if d['name'].lower().startswith(name) and d[field]:
      return d['index']

  raise Exception("Don't understand name %s" % name)

def get_field_names(is_input):
  inout = 'input' if is_input else 'output'
  field = 'max%sChannels' % inout.capitalize()
  return inout, field

def _resolve_index(is_input, name, index, inout, field):
  if name:
    return get_index_field_from_name(is_input, name, field)
  if index < 0:
    index = get_default_device(is_input)['index']
  return index

def get_index_from_config(is_input, get):
  inout, field = get_field_names(is_input)
  name = get('audio', inout, 'device_name')
  index = get('audio', inout, 'device_index')

  return _resolve_index(is_input, name, index, inout, field)

def get_index(is_input, name, index):
  inout, field = get_field_names(is_input)
  return _resolve_index(is_input, name, index, inout, field)

def get_device_info(index):
  return PYAUDIO().get_device_info_by_index(index)

def info():
  return dict((d['index'], _LIST_FORMAT.format(**d)) for d in devices())
