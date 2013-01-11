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

ALLOW_EMPTY_OPTIONS = False

def _add_exception_suffix(e, suffix):
  e.args = tuple(a + suffix for a in e.args)

def recalculate():
  # If running as root, export user pi's home directory as $HOME.
  if getpass.getuser() == 'root':
    os.environ['HOME'] = '/home/pi'

  # Change directory to the echomesh root directory.
  path = dirname(dirname(dirname(abspath(sys.argv[0]))))
  os.chdir(path)

  config = {}

  # Load merged configuration file from the command directory hierarchy.
  for f in reversed(CommandFile.expand('config.yml')):
    try:
      cfg = File.yaml_load(f)
    except:
      raise Exception('Error in configuration file %s' % f)

    try:
      Merge.merge(config, cfg)
    except Exception as e:
      _add_exception_suffix(e, ' in configuration file %s' % f)
      raise

  for i, arg in enumerate(sys.argv):
    if i:
      try:
        cfg = File.yaml_load_stream(arg)
      except:
        raise Exception('Error in command line argument %d: "%s"' % (i, arg))

    try:
      Merge.merge(config, cfg)
    except Exception as e:
      _add_exception_suffix(e, ' in command line argument %d: "%s"' % (i, arg))
      raise


  return config

CONFIG = recalculate()

def is_control_program():
  """is_control_program() is True if Echomesh responds to keyboard commands."""
  return CONFIG.get('control_program', 'enable')

def get(*parts):
  assert parts
  config = CONFIG

  def fail_on_none():
    if config is None and not ALLOW_EMPTY_OPTIONS:
      raise Exception('Empty configuation option for (%s)' % ', '.join(parts))

  for p in parts:
    fail_on_none()

    if type(config) is not dict:
      if config is None:
        config = {}
      else:
        raise Exception("Can't read configuration '%s:'" % ': '.join(parts))

    config = config.get(p, None)

  fail_on_none()
  return config

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

