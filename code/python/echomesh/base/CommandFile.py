from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import re

from compatibility import six

from echomesh.base import Name
from echomesh.base import Merge
from echomesh.base import Path
from echomesh.base import Platform
from echomesh.base import Yaml

TAGS = []

def clean(*path):
  return os.path.join(*path).split('/')

def _command_file(*path):
  path = clean(*path)
  base = Path.ECHOMESH_PATH if path[0] == '4.default' else Path.PROJECT_PATH
  res = os.path.join(base, 'command', *path)
  return res

def _command_path():
  return ([
    '0.local',
    '1.name/' + Name.NAME] +
    [('2.tag/' + t) for t in TAGS] +
    ['3.platform/' + Platform.PLATFORM,
     '4.global',
      _command_file('5.default')])

_COMMAND_PATH = _command_path()

def expand(*path):
  # These first two lines are to make sure we split on / for Windows and others.
  path = clean(*path)
  return [os.path.join('command', i, *path) for i in _COMMAND_PATH]

def resolve(*path):
  for f in expand(*path):
    if os.path.exists(f):
      return f

def load(*path):
  data, error = None, None
  f = resolve(*path)
  if f:
    data = Yaml.read(f)
    if not data:
      error = "Couldn't read Yaml from file %s" % os.path.join(*path)
  else:
    error = "Couldn't find file %s" % os.path.join(*path)

  return data, error

def config_file(scope):
  return _command_file(scope, 'config.yml')

def _recompute_command_path():
  def lookup(name):
    name_map, error = load(name)
    if name_map:
      return Name.lookup(Merge.merge_all(*name_map))

  name = lookup('name_map.yml')
  if name:
    Name.set_name(name)

  tags = lookup('tag_map.yml')
  if tags:
    if isinstance(tags, dict):
      print('Malformed tag_map.yml')
    else:
      if isinstance(tags, six.string_types):
        tags = [tags]
      TAGS[:] = tags
  return _command_path()


_COMMAND_PATH = _recompute_command_path()

_SCOPE_RE = re.compile(r'( (?: [01234]\. )? ) (\w+) ( (?: / \w+ )? ) $', re.X)

_SCOPES = ['local', 'tag', 'name', 'platform', 'global', 'default']

def resolve_scope(scope):
  match = _SCOPE_RE.match(scope)
  if not scope:
    raise Exception("Didn't match: '%s'" % scope)

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

  return '%s%s%s' % (new_prefix, body, suffix)

