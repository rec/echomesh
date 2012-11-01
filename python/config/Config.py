from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os.path
import sys
import yaml

from network import Address
from util import File
from util import Merge

CONFIG_FILE = '~pi/echomesh/config/config.yml'
NODE_CONFIG_FILE = '~pi/echomesh/config/node-config.yml'

# Local configuration for this account.
LOCAL_FILE = '~pi/.echomesh'

# Stores the last dynamic configuration update.
LOCAL_CHANGED_FILE = os.path.expanduser('~pi/.echomesh-changed')

STORE_LOCAL_CHANGED_FILE = True

CONFIG = None

def recalculate():
  global CONFIG

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

def is_enabled(*parts):
  config = CONFIG
  control_program = config.get('control_program', False)
  for p in parts:
    config = config.get(p, {})

  return config.get('enable', not control_program)
