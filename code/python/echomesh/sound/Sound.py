from __future__ import absolute_import, division, print_function, unicode_literals

from cechomesh import get_device_names

def info():
  return {
    'input': ', '.join(get_device_names(True)),
    'output': ', '.join(get_device_names(False)),
    }
