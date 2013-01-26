from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import sys
import weakref

from os.path import abspath, dirname

from echomesh.base import MergeConfig
from echomesh.base import Name
from echomesh.base import Platform

CONFIG = None
CONFIGS_UNVISITED = None  # Report on config items that aren't used.

CLIENTS = []

def add_client(client):
  CLIENTS.append(weakref.ref(client))
  client.config_update()

def update_clients():
  global CLIENTS
  old_clients, CLIENTS = CLIENTS, []
  for c in old_clients:
    cl = c()
    if cl:
      CLIENTS.append(c)
      cl.config_update()

def recalculate(perform_update=False):
  global CONFIG, CONFIGS_UNVISITED
  # If running as root, export user pi's home directory as $HOME.
  if getpass.getuser() == 'root':
    os.environ['HOME'] = '/home/pi'

  local_path = ''
  args = sys.argv[1:]
  if args:
    if not args[0][0] in '{[':
      Name.set_project_path(args[0])

  CONFIG = MergeConfig.merge(args)
  CONFIGS_UNVISITED = copy.deepcopy(CONFIG)
  if perform_update:
    update_clients()

recalculate()

def is_control_program():
  """is_control_program() is True if Echomesh responds to keyboard commands."""
  return get('control_program', 'enable')

def get(*parts):
  config, unvisited = CONFIG, CONFIGS_UNVISITED
  def get_part(config, part):
    if not isinstance(config, dict):
      raise Exception("Reached leaf configuration for %s" % ':'.join(parts))
    value = config.get(part, None)
    if value is None:
      raise Exception("Couldn't find configuration %s" % ':'.join(parts))
    return value

  for part in parts[:-1]:
    config = get_part(config, part)
    if unvisited:
      unvisited = unvisited.get(part, None)

  last_part = parts[-1]
  value = get_part(config, last_part)

  if isinstance(value, dict):
    raise Exception("Didn't reach leaf configuration for %s" % ':'.join(parts))

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



# The following code is all deprecated.
# TODO: find a better way to broadcast persistent changes to all the nodes.

def change(config):
  File.yaml_dump_all(LOCAL_CHANGED_FILE, config)
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1]))


# TODO: a "clear" command that undoes the "change" command.  A tiny bit tricky,
# because we'd have to revert the main config to its original value "in place".

def remove_local():
  os.remove(_config_file('local'))
  global CONFIG
  CONFIG = recalculate()
