from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path

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

def boot(echomesh_instance):
  _close_and_run(echomesh_instance, 'Rebooting', RESTART_CMD)

def halt(echomesh_instance):
  _close_and_run(echomesh_instance, 'Halting this machine', HALT_CMD)

def initialize(echomesh_instance):
  if _halt_allowed():
    echomesh_instance.pause()
    os.execl(*sys.argv)

def _quit(echomesh_instance):
  LOGGER.info('Quitting');
  echomesh_instance.pause()

def update(echomesh_instance):
  LOGGER.info('Pulling latest codebase from github')
  Git.run_git_commands(GIT_UPDATE)
  restart(echomesh_instance)

Register.register_all(
  boot=boot,
  halt=halt,
  initialize=initialize,
  update=update,
  quit=_quit)

def _close_and_run(echomesh_instance, msg, cmd):
  LOGGER.info(msg)
  if _shutdown_allowed():
    Subprocess.run(cmd)
  if _halt_allowed():
    halt(cmd)

# TODO: https://github.com/rec/echomesh/issues/238
def _shutdown_allowed():
  return Config.get('allow_shutdown')

def _halt_allowed():
  return not Config.get('control_program', 'enable')

