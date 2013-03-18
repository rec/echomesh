from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import sys

from echomesh.remote import Register

from echomesh.base import Config
from echomesh.util import Log
from echomesh.util import Subprocess
from gittwit.git import Git

LOGGER = Log.logger(__name__)

SUDO = '/usr/bin/sudo'
SHUTDOWN = '/sbin/shutdown'
HALT_CMD = [SUDO, SHUTDOWN, '-h', 'now']
RESTART_CMD = [SUDO, SHUTDOWN, '-r', 'now']
GIT_UPDATE = ['pull', 'origin', 'master']

def _boot(echomesh_instance):
  _close_and_run(echomesh_instance, 'Rebooting', RESTART_CMD)

def _halt(echomesh_instance):
  _close_and_run(echomesh_instance, 'Halting this machine', HALT_CMD)

def _initialize(echomesh_instance):
  if _allowed('halt'):
    echomesh_instance.pause()
    os.execl(*sys.argv)

def _quit(echomesh_instance):
  LOGGER.info('Quitting')
  echomesh_instance.pause()

def _update(echomesh_instance):
  LOGGER.info('Pulling latest codebase from github')
  Git.run_git_commands(GIT_UPDATE)
  _boot(echomesh_instance)

def _register(function):
  name = function.__name__.strip('_')
  def func(instance):
    if Config.get('permission', name):
      function(instance)
    else:
      LOGGER.error("You don't have permission to run '%s'.", name)
  Register.register(func, name)

for f in [_boot, _halt, _initialize, _update, _quit]:
  _register(f)

def _close_and_run(_, msg, cmd):
  LOGGER.info(msg)
  Subprocess.run(cmd)
  _halt(cmd)

def _allowed(operation):
  return Config.get('permission', operation)
