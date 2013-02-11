from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import os.path
import re

from echomesh.base import CommandFile
from echomesh.base import Merge
from echomesh.base import Yaml
from echomesh.util import FactoryDict
from echomesh.util import UniqueName
from echomesh.util.file import MakeDirs

MANIFEST_NAME = 'manifest.yml'

_BAD_CHARS = re.compile(r'[^-\w\s\d_]+')
_SPACES = re.compile(r'\s+')

class Cache(object):
  def __init__(self, name, suffix):
    if suffix.startswith('.'):
      self.suffix = suffix
    else:
      self.suffix = '.' + suffix

    name_file = CommandFile.clean('cache', name)
    self.cachedir = os.path.abspath(os.path.join(*name_file))
    MakeDirs.makedirs(self.cachedir)
    self.manifest_file = os.path.join(self.cachedir, MANIFEST_NAME)
    self.manifest = Merge.merge(*Yaml.read(self.manifest_file))

  def get_file(self, key):
    return self._get_file_and_new_contents(key)[0]

  def get_contents(self, key):
    filename, contents = self._get_file_and_new_contents(key)
    if contents:
      return contents
    with open(filename, 'rb') as f:
      return f.read()

  def _get_file_contents(self, filename):
    raise Exception('You must override _get_file_contents in your Cache clcass')

  def _get_file_and_new_contents(self, key):
    filename = self.manifest.get(key)
    contents = None
    if not filename:
      fileroot = self._key_to_file(key)
      filename = os.path.join(self.cachedir, fileroot)
      with open(filename, 'wb') as f:
        contents = self._get_file_contents(key)
        f.write(contents)

      self.manifest[key] = fileroot
      Yaml.write(self.manifest_file, self.manifest)
    else:
      filename = os.path.join(self.cachedir, filename)

    return filename, contents

  def _key_to_file(self, key):
    return _SPACES.sub('-', _BAD_CHARS.sub('', key.lower())) + self.suffix

  def _get_file_contents(self, key):
    raise Exception('Must override _get_file_contents')
