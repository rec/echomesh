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

def _local(function, name):
  def f(echomesh_instance):
    if echomesh_instance.broadcasting():
      echomesh_instance.send(type=name)
    else:
      function(echomesh_instance)
  return f

def _remote(function):
  def f(echomesh_instance, **_):
    function(echomesh_instance)
  return f

def _boot(echomesh_instance):
  _close_and_run(echomesh_instance, 'Rebooting', RESTART_CMD)

def _halt(echomesh_instance):
  _close_and_run(echomesh_instance, 'Halting this machine', HALT_CMD)

def _initialize(echomesh_instance):
  if _halt_allowed():
    echomesh_instance.pause()
    os.execl(*sys.argv)

def _exit(echomesh_instance):
  LOGGER.info('Exiting echomesh')
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
  (_exit, 'Exit echomesh instances.', ['halt', 'initialize']),
  (_halt, 'Halt this machine or all machines.', ['boot', 'initialize', 'exit']),
  (_initialize, 'Run the echomesh program from the start here or ' +
   'on all the remote nodes.', ['boot', 'exit', 'halt']),
  (_update, 'Update all the remote nodes from git, then restart them.', []),
  ]

_register()

def _close_and_run(_, msg, cmd):
  LOGGER.info(msg)
  if _shutdown_allowed():
    Subprocess.run(cmd)
  if _halt_allowed():
    _halt(cmd)

# TODO: https://github.com/rec/echomesh/issues/238
def _shutdown_allowed():
  return Config.get('allow_shutdown')

def _halt_allowed():
  return not Config.get('control_program', 'enable')

