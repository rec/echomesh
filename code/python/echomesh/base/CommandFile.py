from __future__ import absolute_import, division, print_function, unicode_literals

from os.path import abspath, dirname, exists, join
import sys

from echomesh.base import File
from echomesh.base import Name
from echomesh.base import Platform

def _compute_levels():
  paths = ['local',
           join('name', Name.NAME),
           join('platform', Platform.PLATFORM),
           'global',
           'default']
  paths = ['%d.%s' % (i, p) for i, p in enumerate(paths)]
  paths[4] = join(Name.ECHOMESH_PATH, 'command', paths[4])
  return paths

_LEVELS = _compute_levels()

def expand(*path):
  # These first two lines are to make sure we split on / for Windows and others.
  filename = '/'.join(path)
  path = filename.split('/')
  retur = [join('command', i, *path) for i in _LEVELS]
  return retur

def resolve(*path):
  for f in expand(*path):
    if exists(f):
      return f

def load_with_error(*path):
  data, error = [], None
  f = resolve(*path)
  if f:
    data = File.yaml_load_all(f) or []
    if not data:
      error = "Couldn't read Yaml from file %s" % '/'.join(path)
  else:
    error = "Couldn't find file %s" % '/'.join(path)

  return data, error

def _recompute_name_from_map():
  name_map, error = load_with_error('name_map.yml')
  if name_map:
    name_map = name_map[0]
    for n in Name.names():
      name = name_map.get(n, None)
      if name:
        Name.set_name(name)
        return

_recompute_name_from_map()
_LEVELS = _compute_levels()
