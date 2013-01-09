from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import os.path
import sys
import yaml

from echomesh.config import Nodes
from echomesh.util import File
from echomesh.util import Merge
from echomesh.util import Platform

ALLOW_EMPTY_OPTIONS = False

def recalculate():
  path = os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0])))
  os.chdir(path)

  # HACK to deal with running as root.
  if getpass.getuser() == 'root':
    os.environ['HOME'] = 'home/pi'

  configs = Nodes.load_all('config.yml')

  if len(sys.argv) > 1:
    configs.append(File.yaml_load(sys.argv[1].strip()))

  return Merge.merge_all(*configs)

CONFIG = recalculate()

def change(config):
  File.yaml_dump_all(LOCAL_CHANGED_FILE, config)
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1]))

# TODO: a "clear" command that undoes the "change" command.  A tiny bit tricky,
# because we'd have to revert the main config to its original value "in place".

def remove_local():
  os.remove(_config_file('local'))
  global CONFIG
  CONFIG = recalculate()

def is_control_program():
  """is_headless() is True if Echomesh responds to keyboard commands."""
  return CONFIG.get('control_program', 'enable')

def get(*parts):
  assert parts
  config = CONFIG

  def fail_on_none():
    if config is None and not ALLOW_EMPTY_OPTIONS:
      raise Exception('Empty configuation option for (%s)' % ', '.join(parts))

  for p in parts:
    fail_on_none()
    if config is None:
      config = {}

    config = config.get(p, None)

  fail_on_none()
  return config
