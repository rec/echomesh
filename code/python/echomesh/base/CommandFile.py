from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

import six

from echomesh.base import Name
from echomesh.base import Merge
from echomesh.base import Path
from echomesh.base import Platform
from echomesh.base import Yaml

def clean(*path):
  return os.path.join(*path).split('/')

def _command_file(*path):
  path = clean(*path)
  base = Path.ECHOMESH_PATH if path[0] == '4.default' else Path.PROJECT_PATH
  res = os.path.join(base, 'command', *path)
  return res

COMMAND_PATH = None

def compute_command_path():
  global COMMAND_PATH
  COMMAND_PATH = ([
    '1.name/' + Name.NAME] +
    [('2.tag/' + t) for t in Name.TAGS] +
    ['3.platform/' + Platform.PLATFORM,
     '4.master',
      _command_file('5.default')])

compute_command_path()

def expand(*path):
  # These first two lines are to make sure we split on / for Windows and others.
  path = clean(*path)
  return [os.path.join('command', i, *path) for i in COMMAND_PATH]

def resolve(*path):
  x = expand(*path)
  for f in x:
    if os.path.exists(f):
      return f

def load(*path):
  f = resolve(*path)
  if f:
    data = Yaml.read(f)
    if data:
      return data

  raise Exception("Couldn't read Yaml from file %s" % os.path.join(*path))

def config_file(scope):
  return _command_file(scope, 'config.yml')

