from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import shutil
import six

from echomesh.remote import RemoteRegistry

from echomesh.base import Config
from echomesh.base import MakeDirs
from echomesh.base import Path

def transfer(_, **data):
  backup_directory = os.path.join(Path.DATA_PATH, '.echomesh-xfer')

  try:
    shutil.rmtree(backup_directory)
  except OSError:
    pass

  directories = data.get('directories', [])
  if '' in directories:
    directories = os.listdir(Path.DATA_PATH)

  for directory in directories:
    parent = os.path.dirname(os.path.join(backup_directory, directory))
    MakeDirs.parent_makedirs(parent)
    shutil.move(os.path.join(Path.DATA_PATH, directory), parent)

  for f, value in six.iteritems(data.get('files')):
    fname = os.path.join(Path.DATA_PATH, f)
    MakeDirs.parent_makedirs(fname)
    with open(fname, 'w') as o:
      o.write(value['contents'])
    os.utime(fname, (value['atime'], value['mtime']))

  if Config.get('delete_backups_after_transfer'):
    try:
      shutil.rmtree(backup_directory)
    except:
      pass

HELP = """transfer:  transfer all your files to all the other echomesh nodes.
"""
