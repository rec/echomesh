from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import DataFileName
from echomesh.base import Name
from echomesh.base import Path
from echomesh.base import Platform
from echomesh.base import Yaml

_DATA_PATH = None
_DATA_PATH_NAMES = None

def clean(*path):
  return os.path.join(*path).split('/')

def _command_file(*path):
  path = clean(*path)
  if path[0] == 'default':
    return os.path.join(Path.PYTHON_PATH, 'echomesh', 'config', *path[1:])
  else:
    return os.path.join(Path.PROJECT_PATH, 'data', *path)

def compute_command_path(force=False):
  global _DATA_PATH, _DATA_PATH_NAMES
  if _DATA_PATH and not force:
    return
  _DATA_PATH = (['name/' + Name.NAME] +
               [('tag/' + t) for t in Name.TAGS] +
               ['platform/' + Platform.PLATFORM,
                'master',
                _command_file('default/platform/%s' % Platform.PLATFORM),
                _command_file('default')])

  _DATA_PATH_NAMES = (['name'] +  # TODO: fix?
                     [('tag/' + t) for t in Name.TAGS] +
                     ['platform/' + Platform.PLATFORM,
                      'master',
                      'default/platform/%s' % Platform.PLATFORM,
                      'default'])

def named_paths():
  compute_command_path()
  return zip(_DATA_PATH_NAMES, _DATA_PATH)

def _expand(*path):
  # These first two lines are to make sure we split on / for Windows and others.
  path = clean(*path)
  compute_command_path()
  return [os.path.join('data', i, *path) for i in _DATA_PATH]

def expand_config():
  return _expand('config', 'config.yml')[:-2] + _expand('config.yml')[-2:]

def resolve(*path):
  for f in _expand(*path):
    try:
      return DataFileName.data_filename(f)
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
  if scope.startswith('default'):
    return _command_file(scope, 'config', 'config.yml')
  else:
    return _command_file(scope, 'config.yml')
