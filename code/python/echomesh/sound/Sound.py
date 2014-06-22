from __future__ import absolute_import, division, print_function, unicode_literals

try:
  from cechomesh import get_device_names
except ImportError:
  get_device_names = lambda x: '(none)',

def info():
  return {
    'input': ', '.join(get_device_names(True)),
    'output': ', '.join(get_device_names(False)),
    }
