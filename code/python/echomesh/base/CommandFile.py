from __future__ import absolute_import, division, print_function, unicode_literals

from os.path import exists, join

from echomesh.base import Address

NAME = Address.NODENAME

def _compute_levels():
  from echomesh.base import Platform

  paths = ['local',
           join('name', NAME),
           join('platform', Platform.PLATFORM),
           'global',
           'default']
  return ['%d.%s' % (i, p) for i, p in enumerate(paths)]

_LEVELS = _compute_levels()

def expand(*path):
  # These first two lines are to make sure we split on / for Windows and others.
  filename = '/'.join(path)
  path = filename.split('/')
  return [join('command', i, *path) for i in _LEVELS]

def resolve(*path):
  for f in expand(*path):
    if exists(f):
      return f

def load_with_error(*path):
  data, error = [], None
  f = resolve(*path)
  if f:
    from echomesh.base import File

    data = File.yaml_load_all(f) or []
    if not data:
      error = "Couldn't read Yaml from file %s" % '/'.join(path)
  else:
    error = "Couldn't find file %s" % '/'.join(path)

  return data, error

def _recompute_name():
  name_map, error = load_with_error('name_map.yml')
  if name_map:
    name_map = name_map[0]
    for n in Address.NAMES:
      name = name_map.get(n)
      if name:
        return name
  return NAME

NAME = _recompute_name()
_LEVELS = _compute_levels()
