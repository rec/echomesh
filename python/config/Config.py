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

def _config_file(node):
  return os.path.join('nodes', node, 'config.yml')

def _load(node):
  return File.yaml_load(_config_file(node))

def recalculate():
  path = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
  os.chdir(path)

  # HACK to deal with running as root.
  if getpass.getuser() == 'root':
    os.environ['HOME'] = 'home/pi'

  configs = [_load('global'), _load(Address.NODENAME), _load('local')]

  if len(sys.argv) > 1:
    configs.append(File.yaml_load(sys.argv[1].strip()))

  return Merge.merge_all(*configs)

CONFIG = recalculate()

def change(config):
  File.yaml_dump_all(LOCAL_CHANGED_FILE, config)
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1]))

def remove_local():
  os.remove(_config_file('local'))
  global CONFIG
  CONFIG = recalculate()

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
  assert config
  for p in parts[:-1]:
    config = config.get(p, {})
    if config is None:
      config = {}
  return config.get(parts[-1], default)

def is_enabled(*parts):
  return get(parts + ('enable',), not is_headless())
