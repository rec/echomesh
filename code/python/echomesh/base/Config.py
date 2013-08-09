from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import six

from compatibility.weakref import WeakSet

from echomesh.base import Args
from echomesh.base import CommandFile
from echomesh.base import MergeConfig
from echomesh.base import Name
from echomesh.base import Path

MERGE_CONFIG = None
CONFIGS_UNVISITED = None  # Report on config items that aren't used.

CLIENTS = WeakSet()

THROW_EXCEPTIONS = True

def reconfigure():
  global MERGE_CONFIG, CONFIGS_UNVISITED

  # Read a configuration file with a given name, tags, and project.
  def _make(name, tags, project, show_error, prompt):
    Name.set_name(name)
    Name.set_tags(tags)
    Path.set_project_path(project_path=project, show_error=show_error)

    CommandFile.compute_command_path()
    return MergeConfig.MergeConfig()

  # First, make a config with the default information.
  merge_config = _make(None, [], None, False, False)

  # Now, use the name, tags and project to get the correct configuration.
  get = merge_config.config.get

  name = get('name') or Name.lookup(get('map', {}).get('name', {}))
  tags = get('tag') or Name.lookup(get('map', {}).get('tag', {})) or []
  project = get('project')

  if not isinstance(tags, (list, tuple)):
    tags = [tags]

  MERGE_CONFIG = _make(name, tags, project, True, prompt=not get('autostart'))
  CONFIGS_UNVISITED = copy.deepcopy(MERGE_CONFIG.config)

def add_client(client):
  if not client in CLIENTS:
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
  config, unvisited = MERGE_CONFIG.config, CONFIGS_UNVISITED
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

def assign(values):
  return MERGE_CONFIG.assign(values)

def get_unvisited():
  def fix(d):
    if isinstance(d, dict):
      for k, v in list(six.iteritems(d)):
        assert v is not None
        fix(v)
        if v == {}:
          del d[k]
    return d
  if not True:
    return CONFIGS_UNVISITED
  return fix(copy.deepcopy(CONFIGS_UNVISITED))

