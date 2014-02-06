from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import sys

from echomesh.base import Config
from echomesh.base import Path
from echomesh.command import REGISTRY
from echomesh.remote import RemoteRegistry
from echomesh.util import Log
from echomesh.base import Quit
from echomesh.util import Subprocess
from gittwit.git import Git

LOGGER = Log.logger(__name__)

SUDO = '/usr/bin/sudo'
SHUTDOWN = '/sbin/shutdown'
HALT_CMD = [SUDO, SHUTDOWN, '-h', 'now']
RESTART_CMD = [SUDO, SHUTDOWN, '-r', 'now']
GIT_UPDATE = ['pull', 'origin', 'master']
DEFAULT_SHELL = '/bin/bash'
INITIALIZE_ENABLED = False

def _remote(function):
  def f(echomesh_instance, **_):
    name = function.__name__.strip('_')
    if Config.get('permission', name):
      function(echomesh_instance)
    else:
      LOGGER.error("You don't have permission to run '%s'.", name)
  return f

def _local(function, name):
  local_fn = _remote(function)
  def f(echomesh_instance):
    if echomesh_instance.broadcasting():
      echomesh_instance.send(type=name)
    else:
      local_fn(echomesh_instance)
  return f

def _boot(echomesh_instance):
  _close_and_run(echomesh_instance, 'Rebooting', RESTART_CMD)

def _exec(_, cmd):
  result, code = Subprocess.run(cmd)
  if code:
    LOGGER.error('%s (%d)', result, code)
  else:
    LOGGER.info('%s', result)

def _halt(echomesh_instance):
  _close_and_run(echomesh_instance, 'Halting this machine', HALT_CMD)

def _initialize(echomesh_instance):
  if INITIALIZE_ENABLED:
    echomesh_instance.pause()
    shell = os.getenv('SHELL', DEFAULT_SHELL)
    LOGGER.info('Echomesh is restarting.')
    os.execl(shell, shell, *sys.argv)
  else:
    _quit(echomesh_instance)

def _quit(_):
  Quit.request_quit()
  return True

def _update(echomesh_instance):
  LOGGER.info('Pulling latest codebase from github.')
  directory = os.getcwd()

  try:
    os.chdir(Path.echomesh_path())
    Git.run_git_commands(GIT_UPDATE)
    _initialize(echomesh_instance)
    if not INITIALIZE_ENABLED:
      LOGGER.info('Please restart echomesh to see the updated changes.')
  finally:
    os.chdir(directory)

_UPDATE_HELP = """
The "update" command updates the echomesh code to the latest version in github.

It updates all the echomesh nodes that have been discovered on your network -
just type

  update

at the echomesh prompt and everything should proceed automatically.
"""

def _register():
  for cmd, help_text, see_also in COMMANDS:
    name = cmd.__name__.strip('_')
    REGISTRY.register(_local(cmd, name), name, help_text, see_also)
    RemoteRegistry.register(_remote(cmd), name)

COMMANDS = [
  (_boot, 'Reboot this machine or all machines.', ['initialize', 'halt']),
  (_exec, 'Execute a shell command on this machine.', []),
  (_quit, 'Quit echomesh instances.', ['halt', 'initialize']),
  (_halt, 'Halt this machine or all machines.', ['boot', 'initialize', 'quit']),
  (_initialize, 'Run the echomesh program from the start here or ' +
   'on all the remote nodes.', ['boot', 'quit', 'halt']),
  (_update, _UPDATE_HELP, []),
  ]

_register()

def _close_and_run(_, msg, cmd):
  LOGGER.info(msg)
  if _allowed('shutdown'):
    Subprocess.run(cmd)
  if _allowed('halt'):
    _halt(cmd)

def _allowed(operation):
  return Config.get('permission', operation)
