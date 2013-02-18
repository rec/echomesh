from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.remote import Register

from echomesh.base import Config
from echomesh.util import Log
from echomesh.util import Subprocess
from gittwit.git import Git

LOGGER = Log.logger(__name__)

SUDO = '/usr/bin/sudo'
SHUTDOWN = '/sbin/shutdown'
SHUTDOWN_CMD = [SUDO, SHUTDOWN, '-h', 'now']
RESTART_CMD = [SUDO, SHUTDOWN, '-r', 'now']
GIT_UPDATE = ['pull', 'origin', 'master']

def halt(echomesh):
  if _halt_allowed():
    LOGGER.info('Quitting');
    echomesh.stop()

def restart(echomesh):
  _close_and_run(echomesh, 'Restarting', RESTART_CMD)

def shutdown(echomesh):
  _close_and_run(echomesh, 'Shutting down', SHUTDOWN_CMD)

def update(echomesh):
  LOGGER.info('Pulling latest codebase from github')
  Git.run_git_commands(GIT_UPDATE)
  restart(echomesh)

Register.register_all(
  halt=halt,
  restart=restart,
  shutdown=shutdown,
  update=update)

def _close_and_run(echomesh, msg, cmd):
  LOGGER.info(msg)
  if _shutdown_allowed():
    Subprocess.run(cmd)
  if _halt_allowed():
    halt(cmd)

def _shutdown_allowed():
  return Config.get('allow_shutdown')

def _halt_allowed():
  return not Config.get('control_program', 'enable')

