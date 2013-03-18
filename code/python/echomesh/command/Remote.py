from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import sys

from echomesh.base import Config
from echomesh.util import Log
from echomesh.util import Subprocess
from gittwit.git import Git
import echomesh.command.Register
import echomesh.remote.Register

LOGGER = Log.logger(__name__)

SUDO = '/usr/bin/sudo'
SHUTDOWN = '/sbin/shutdown'
HALT_CMD = [SUDO, SHUTDOWN, '-h', 'now']
RESTART_CMD = [SUDO, SHUTDOWN, '-r', 'now']
GIT_UPDATE = ['pull', 'origin', 'master']

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

def _halt(echomesh_instance):
  _close_and_run(echomesh_instance, 'Halting this machine', HALT_CMD)

def _initialize(echomesh_instance):
  echomesh_instance.pause()
  os.execl(*sys.argv)

def _quit(echomesh_instance):
  echomesh_instance.pause()
  echomesh_instance.quitting = True
  return True

def _update(echomesh_instance):
  LOGGER.info('Pulling latest codebase from github')
  Git.run_git_commands(GIT_UPDATE)
  _boot(echomesh_instance)

def _register():
  for cmd, help_text, see_also in COMMANDS:
    name = cmd.__name__.strip('_')
    echomesh.command.Register.register(_local(cmd, name), name,
                                       help_text, see_also)
    echomesh.remote.Register.register(_remote(cmd), name)

COMMANDS = [
  (_boot, 'Reboot this machine or all machines.', ['initialize', 'halt']),
  (_quit, 'Quit echomesh instances.', ['halt', 'initialize']),
  (_halt, 'Halt this machine or all machines.', ['boot', 'initialize', 'quit']),
  (_initialize, 'Run the echomesh program from the start here or ' +
   'on all the remote nodes.', ['boot', 'quit', 'halt']),
  (_update, 'Update all the remote nodes from git, then restart them.', []),
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
