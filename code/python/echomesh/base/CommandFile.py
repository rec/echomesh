from __future__ import absolute_import, division, print_function, unicode_literals

from os.path import abspath, dirname, exists, join
import re
import sys

from echomesh.base import File
from echomesh.base import Name
from echomesh.base import Platform

def clean(*path):
  return '/'.join(path).split('/')

def expand(*path):
  # These first two lines are to make sure we split on / for Windows and others.
  filename = '/'.join(path)
  path = filename.split('/')
  retur = [join('command', i, *path) for i in _LEVELS]
  return retur

def _command_file(*path):
  path = clean(*path)
  base = Name.ECHOMESH_PATH if path[0] == '4.default' else Name.PROJECT_PATH
  res = join(base, 'command', *path)
  return res

def _compute_levels():
  paths = ['local',
           join('name', Name.NAME),
           join('platform', Platform.PLATFORM),
           'global',
           'default']
  paths = ['%d.%s' % (i, p) for i, p in enumerate(paths)]
  paths[4] = _command_file(paths[4])
  return paths

_LEVELS = _compute_levels()

def resolve(*path):
  for f in expand(*path):
    if exists(f):
      return f

def load_with_error(*path):
  data, error = None, None
  f = resolve(*path)
  if f:
    data = File.yaml_load_all(f)
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

_SCOPE_RE = re.compile(r'( (?: [01234]\. )? ) (\w+) ( (?: /\w+ )? ) $', re.X)

_SCOPES = ['local', 'name', 'platform', 'global', 'default']

def resolve_scope(scope):
  match = _SCOPE_RE.match(scope)
  if not scope:
    raise Exception("Didn't match: '%s'", scope)

  prefix, body, suffix = match.groups()
  if body not in _SCOPES:
    raise Exception("Didn't understand body %s" % body)

  new_prefix = '%d.' % _SCOPES.index(body)
  if prefix and prefix != new_prefix:
    raise Exception("Wrong prefix %s" % body)

  if body == 'name':
    suffix = suffix or ('/' + Name.NAME)

  elif body == 'platform':
    suffix = suffix or ('/' + Platform.PLATFORM)

  elif suffix:
    raise Exception("Name not needed for %s" % body)

  return '%s%s%s' % new_prefix, body, suffix

def scope_file(scope, *path):
  return _command_file(resolve_scope(scope), *path)
