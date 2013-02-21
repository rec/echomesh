from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import shutil

from echomesh.base import Config
from echomesh.base import Path
from echomesh.base import Yaml
from echomesh.util import Log
from echomesh.util.file import MakeDirs
from echomesh.util import Scope

LOGGER = Log.logger(__name__)

class Transfer(object):
  def __init__(self):
    self.bulk_mode = False
    self.bulk_transfer = {}
    self.backup_directory = os.path.join(Path.COMMAND_PATH, '.echomesh-xfer')

  def start_bulk(self):
    self.bulk_mode = True

  def stop_bulk(self):
    self.move_directory()
    for f, contents in self.bulk_tranfer.iteritems():
      self.write_file(f, contents)
    self.bulk_mode = False
    self.bulk_tranfer = {}
    if Config.get('delete_backups_after_transfer'):
      self.delete_directory()

  def transfer(self, data):
    f, contents = data['file'], data['contents']
    if self.bulk_mode:
      self.bulk_transfer[f] = contents
    else:
      self.write_file(f, contents)

  def move_directory(self):
    self.delete_directory()
    os.mkdir(self.backup_directory)
    for scope in Scope.SCOPE_DIRECTORIES[:-1]:
      shutil.move(os.path.join(self.backup_directory, scope),
                  self.backup_directory)

  def delete_directory(self):
    shutil.rmtree(self.backup_directory)

  def write_file(f, contents):
    fname = os.path.join(Path.COMMAND_PATH, f)
    MakeDirs.parent_makedirs(fname)
    with open(fname, 'w') as o:
      o.write(Yaml.encode_one(contents))
