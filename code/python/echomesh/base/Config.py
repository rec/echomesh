from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import six

from os.path import abspath, dirname

from compatibility.weakref import WeakSet

from echomesh.base import CommandFile
from echomesh.base import MergeConfig
from echomesh.base import Name
from echomesh.base import Platform

CONFIG = None
CONFIGS_UNVISITED = None  # Report on config items that aren't used.

CLIENTS = WeakSet()
ARGUMENTS = []

def add_client(client):
  CLIENTS.add(client)
  client.config_update(get)

def update_clients():
  for c in CLIENTS:
    cl.config_update(get)

def recalculate(perform_update=False, args=None):
  if args:
    global ARGUMENTS
    ARGUMENTS = args[1:]

  # If running as root, export user pi's home directory as $HOME.
  if getpass.getuser() == 'root':
    os.environ['HOME'] = '/home/pi'

  global CONFIG, CONFIGS_UNVISITED

  # Do this the first time to get everything before tag and name resolution.
  CONFIG = MergeConfig.merge_config()
  CONFIGS_UNVISITED = copy.deepcopy(CONFIG)

  name = Name.lookup(get('map', 'name'))
  if name:
    Name.set_name(name)

  tags = Name.lookup(get('map', 'tags'))
  if tags:
    if isinstance(tags, six.string_types):
      tags = [tags]
    Name.TAGS = tags

  if name or tags:
    CommandFile.compute_command_path()

  if perform_update:
    update_clients()

def get(*parts):
  config, unvisited = CONFIG, CONFIGS_UNVISITED
  none = object()
  def get_part(config, part):
    if not isinstance(config, dict):
      raise Exception("Reached leaf configuration for %s" % ':'.join(parts))
    value = config.get(part, none)
    if value is none:
      raise Exception("Couldn't find configuration %s" % ':'.join(parts))
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
