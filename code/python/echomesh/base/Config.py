from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import six

from compatibility.weakref import WeakSet

from echomesh.base import CommandFile
from echomesh.base import MergeConfig
from echomesh.base import Name

CONFIG = None
CONFIGS_UNVISITED = None  # Report on config items that aren't used.

CLIENTS = WeakSet()

THROW_EXCEPTIONS = True

def recalculate():
  _fix_home_directory_environment_variable()
  _reset_configs()
  _get_name_and_tags()

def add_client(client):
  CLIENTS.add(client)
  client.config_update(get)

def update_clients():
  for c in CLIENTS:
    try:
      c.config_update(get)
    except:
      if THROW_EXCEPTIONS:
        raise

def get(*parts):
  config, unvisited = CONFIG, CONFIGS_UNVISITED
  none = object()
  def get_part(config, part):
    if not isinstance(config, dict):
      raise Exception("Reached leaf configuration for %s: %s" %
                      ('.'.join(parts), config))
    value = config.get(part, none)
    if value is none:
      raise Exception('Couldn\'t find configuration "%s"' % '.'.join(parts))
    return value

  for part in parts[:-1]:
    config = get_part(config, part)
    if unvisited:
      unvisited = unvisited.get(part)

  last_part = parts[-1]
  value = get_part(config, last_part)

  try:
    del unvisited[last_part]
  except:
    pass

  return value

def get_unvisited():
  def fix(d):
    if isinstance(d, dict):
      for k, v in list(d.iteritems()):
        assert v is not None
        fix(v)
        if v == {}:
          del d[k]
    return d
  if not True:
    return CONFIGS_UNVISITED
  return fix(copy.deepcopy(CONFIGS_UNVISITED))

def _fix_home_directory_environment_variable():
  # If running as root, export user pi's home directory as $HOME.
  if getpass.getuser() == 'root':
    os.environ['HOME'] = '/home/pi'

def _reset_configs():
  global CONFIG, CONFIGS_UNVISITED

  # Do this the first time to get everything before tag and name resolution.
  CONFIG = MergeConfig.merge_config()
  CONFIGS_UNVISITED = copy.deepcopy(CONFIG)

def _get_name_and_tags():
  name = Name.lookup(get('map', 'name'))
  if name:
    Name.set_name(name)

  tags = Name.lookup(get('map', 'tag'))
  if tags:
    if isinstance(tags, six.string_types):
      tags = [tags]
    Name.TAGS = tags

  if name or tags:
    CommandFile.compute_command_path()

