from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import Name
from echomesh.base import Path
from echomesh.base import Platform
from echomesh.base import Yaml

COMMAND_PATH = None
COMMAND_PATH_NAMES = None

def clean(*path):
  return os.path.join(*path).split('/')

def _command_file(*path):
  path = clean(*path)
  if path[0] == 'default':
    return os.path.join(Path.CODE_PATH, 'echomesh', 'config', *path[1:])
  else:
    return os.path.join(Path.PROJECT_PATH, 'command', *path)

COMMAND_PATH = None
def compute_command_path():
  global COMMAND_PATH, COMMAND_PATH_NAMES
  COMMAND_PATH = (['name/' + Name.NAME] +
                  [('tag/' + t) for t in Name.TAGS] +
                  ['platform/' + Platform.PLATFORM,
                   'master',
                   _command_file('default/platform/%s' % Platform.PLATFORM),
                   _command_file('default')])

  COMMAND_PATH_NAMES = (['name'] +  # TODO: fix?
                        [('tag/' + t) for t in Name.TAGS] +
                        ['platform/' + Platform.PLATFORM,
                         'master',
                         'default/platform/%s' % Platform.PLATFORM,
                         'default'])

compute_command_path()

def named_paths():
  return zip(COMMAND_PATH_NAMES, COMMAND_PATH)

def expand(*path):
  # These first two lines are to make sure we split on / for Windows and others.
  path = clean(*path)
  return [os.path.join('command', i, *path) for i in COMMAND_PATH]

def resolve(*path):
  x = expand(*path)
  for f in x:
    try:
      return Yaml.filename(f)
    except:
      continue

def load_resolve(*path):
  f = resolve(*path)
  if f:
    data = Yaml.read(f)
    if data:
      return f, data

  raise Exception("Couldn't read Yaml from file %s" % os.path.join(*path))

def load(*path):
  return load_resolve(*path)[1]

def base_file(*path):
  return _command_file('master', *path)

def config_file(scope='default'):
  return _command_file(scope, 'config.yml')

def read_config(scope='default'):
  return Yaml.read(config_file(scope))
