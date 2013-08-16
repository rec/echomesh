from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import Config
from echomesh.base import Path
from echomesh.util import Log
from echomesh.util.dict.PersistentDict import PersistentDict

LOGGER = Log.logger(__name__)

ALIAS_FILE_NAME = 'aliases.yml'
ALIAS_DOTFILE_NAME = '.aliases.yml'
_INSTANCE = None
_CLIENT = None

class Aliases(object):
  INSTANCE = None
  DICT = None

  def __init__(self):
    Config.add_client(self)

  def config_update(self, get):
    if get('aliases', 'save_with_project'):
      filename = os.path.join(Path.PROJECT_PATH, ALIAS_FILE_NAME)
    else:
      filename = os.path.join(os.path.expanduser('~'), ALIAS_DOTFILE_NAME)
    if Aliases.DICT:
      Aliases.DICT.set_filename(filename)
    else:
      Aliases.DICT = PersistentDict(filename)

def instance():
  if not Aliases.INSTANCE:
    Aliases.INSTANCE = Aliases()

  return Aliases.DICT
