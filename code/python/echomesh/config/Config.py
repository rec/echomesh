from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import sys
import yaml

from os.path import abspath, dirname

import yaml

from echomesh.config import CommandFile
from echomesh.util import Merge
from echomesh.util import Platform
from echomesh.util.file import File

# If running as root, export user pi's home directory as $HOME.
if getpass.getuser() == 'root':
  os.environ['HOME'] = '/home/pi'

# Change directory to the echomesh root directory.
path = dirname(dirname(dirname(abspath(sys.argv[0]))))
os.chdir(path)

def _add_exception_suffix(e, suffix):
  e.args = tuple(a + suffix for a in e.args)

def _merge_level_files():
  # Load merged configuration file from the command directory hierarchy.
  config = None
  for f in reversed(CommandFile.expand('config.yml')):
    try:
      cfg = File.yaml_load(f)
    except:
      raise Exception('Error in configuration file %s' % f)

    if config is None:
      config = cfg
    else:
      try:
        Merge.merge(config, cfg)
      except Exception as e:
        _add_exception_suffix(e, ' in configuration file %s' % f)
        raise
  return config

def _merge_command_line_arguments(config):
  for i, arg in enumerate(sys.argv):
    if i:
      try:
        cfgs = File.yaml_load_stream(arg)
      except:
        raise Exception('Error in command line argument %d: "%s"' % (i, arg))

      try:
        Merge.merge_all(config, *cfgs)
      except Exception as e:
        _add_exception_suffix(e, ' in command line argument %d: "%s"' % (i, arg))
        raise
  return config

CONFIG = _merge_command_line_arguments(_merge_level_files())

def is_control_program():
  """is_control_program() is True if Echomesh responds to keyboard commands."""
  return CONFIG.get('control_program', 'enable')

# Report on config items that aren't used.
CONFIGS_UNVISITED = copy.deepcopy(CONFIG)

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
    unvisited = get_parent(unvisited, part)

  last_part = parts[:-1]
  valuee = get_part(config, last_part)

  if isinstance(config, dict):
    raise Exception("Didn't reach leaf configuration for %s" % ':'.join(parts))

  CONFIGURATION

  return value


# The following code is all deprecated.
# TODO: find a better way to broadcast persistent changes to all the nodes.

def change(config):
  File.yaml_dump_all(LOCAL_CHANGED_FILE, config)
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1]))


# def unused_config():


# TODO: a "clear" command that undoes the "change" command.  A tiny bit tricky,
# because we'd have to revert the main config to its original value "in place".

def remove_local():
  os.remove(_config_file('local'))
  global CONFIG
  CONFIG = recalculate()

