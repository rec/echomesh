from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import os.path
import sys
import yaml

from network import Address
from util import File
from util import Merge
from util import Platform

CONFIG_FILE = 'config/config.yml'
NODE_CONFIG_FILE = 'config/node-config.yml'

# Local configuration for this account.
LOCAL_FILE = 'local/config.yml'

# Stores the last dynamic configuration update.
LOCAL_CHANGED_FILE = 'local/config-changed.yml'

STORE_LOCAL_CHANGED_FILE = True

CONFIG = None

def recalculate():
  global CONFIG

  # HACK to deal with running as root.
  if getpass.getuser() == 'root':
    os.environ['HOME'] = 'home/pi'

  CONFIG = Merge.merge_into_all(
    File.yaml_load(CONFIG_FILE),
    File.yaml_load(NODE_CONFIG_FILE.strip()).get(Address.NODENAME, {}),
    File.yaml_load(LOCAL_FILE),
    File.yaml_load(LOCAL_CHANGED_FILE))

  if len(sys.argv) > 1:
    Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1].strip()))

recalculate()

def change(config):
  File.yaml_dump_all(LOCAL_CHANGED_FILE, config)
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1]))

def remove_local():
  os.remove(LOCAL_CHANGED_FILE)
  recalculate()

# TODO: a "clear" command that undoes the "change" command.  A tiny bit tricky,
# because we'd have to revert the main config to its original value "in place".

def is_control_program():
  """is_headless() is True if Echomesh responds to keyboard commands."""
  return CONFIG.get('control_program', not Platform.IS_LINUX)

def is_headless():
  """is_headless() is True if Echomesh cannot do graphics, sound or scores."""
  return CONFIG.get('headless', not Platform.IS_LINUX)

def get(parts, default=None):
  assert parts

  config = CONFIG
  for p in parts[:-1]:
    config = config.get(p, {})
  return config.get(parts[-1], default)

def is_enabled(*parts):
  return get(parts + ('enable',), not is_headless())
