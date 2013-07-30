from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.util import Importer

ERROR_MESSAGE = ('You requested a feature that needs the Python library ' +
                 '"%s", which has been disabled in your Config')

def imp(module):
  if Config.get('load_module', module):
    return Importer.imp(module)
  else:
    return Importer.FailedImport(ERROR_MESSAGE % module)
