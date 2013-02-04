from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import os.path
import re

from echomesh.base import CommandFile
from echomesh.base import File
from echomesh.util import FactoryDict
from echomesh.util import UniqueName
from echomesh.util.file import MakeDirs

MANIFEST_NAME = 'manifest.yml'

_BAD_CHARS = re.compile(r'[^\w\s]+')

class CacheDirectory(object):
  def __init__(self, name):
    self.cachedir = CommandFile.clean('cache', name)
    MakeDirs.makedirs(self.cachedir)
    self.manifest_file = os.join(self.cachedir, MANIFEST_NAME)
    self.manifest = File.yaml_load(self.manifest_file)

  def get_file(self, key):
    return self._get_file_and_new_contents()[0]

  def get_contents(self, key):
    filename, contents = self._get_file_and_new_contents()
    if contents:
      return contents
    with open(filename, 'rb') as f:
      return f.read()

  def _get_file_and_new_contents(self, key):
    filename = self.manifest.get(key)
    contents = None
    if not filename:
      filename = self._key_to_file(key)
      with open(filename, 'wb') as f:
        contents = self._get_file_contents(key)
        f.write(contents)

      self._fill_file(filename)
      self.manifest[key] = filename
      File.yaml_dump_one(self.manifest)

    return filename, contents

  def _key_to_file(self, key):
    return _BAD_CHARS.sub('', key.lower())

  def _get_file_contents(self, key):
    raise Exception('Must override _get_file_contents')

