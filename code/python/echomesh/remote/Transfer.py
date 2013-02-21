from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path

from echomesh.remote import Register

from echomesh.base import Config
from echomesh.base import Path
from echomesh.base import Yaml
from echomesh.util import Log
from echomesh.util.file import MakeDirs

LOGGER = Log.logger(__name__)

def transfer(echomesh, **data):
  backup_directory = os.path.join(Path.COMMAND_PATH, '.echomesh-xfer')
  shutil.rmtree(backup_directory)

  if '.' in directories:
    directories = os.listdir(Path.COMMAND_PATH)

  for directory in data.get('directories', []):
    parent = os.dirname(os.path.join(backup_directory, directory))
    MakeDirs.parent_makedirs(parent)
    shutil.move(os.path.join(Path.COMMAND_PATH, directory), parent)

  for f, contents in data.get('files').iteritems():
    fname = os.path.join(Path.COMMAND_PATH, f)
    MakeDirs.parent_makedirs(fname)
    with open(fname, 'w') as o:
      o.write(Yaml.encode_one(contents))

  if Config.get('delete_backups_after_transfer'):
    try:
      shutil.rmtree(backup_directory)
    except:
      pass

Register.register_all(transfer=transfer)
