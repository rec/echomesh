from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from config import Config
from git import Git
from util import Log
from util import Subprocess

LOGGER = Log.logger(__name__)

SUDO = '/usr/bin/sudo'
SHUTDOWN = '/sbin/shutdown'
SHUTDOWN_CMD = [SUDO, SHUTDOWN, '-h', 'now']
RESTART_CMD = [SUDO, SHUTDOWN, '-r', 'now']
GIT_UPDATE = ['pull', 'origin', 'master']

class Router(object):
  def __init__(self, echomesh, clients):
    self.echomesh = echomesh
    self.clients = clients

  def clear(self, data):
    self.echomesh.remove_local()

  def client(self, data):
    self.clients.new_client(data)

  def config(self, msg):
    config = msg.get('data', None)
    if data:
      self.echomesh.set_config(config)
    else:
      LOGGER.error('Empty config data received')

  def event(self, event):
    self.echomesh.receive_event(event)

  def halt(self, data):
    if not self._is_control_program():
      LOGGER.info('Quitting');
      self.echomesh.close()

  def score(self, msg):
    score = msg.get('data', None)
    if score:
      self.echomesh.set_score(score)
    else:
      LOGGER.error('Empty score data received')
    self._error(data)

  def restart(self, data):
    self._close_and_run('Restarting', RESTART_CMD)

  def shutdown(self, data):
    self._close_and_run('Shutting down', SHUTDOWN_CMD)

  def update(self, event):
    LOGGER.info('Pulling latest codebase from github')
    Git.run_git_commands(GIT_UPDATE)
    self.restart(event)

  # TODO!
  def rerun(self, data):
    self._error(data)

  def start(self, data):
    self._error(data)

  def stop(self, data):
    self._error(data)

  def _error(self, data):
    LOGGER.error("Command '%s' not implemented", data['type'])

  def _close_and_run(self, msg, cmd):
    LOGGER.info(msg)
    if not self._is_control_program() and self.config['allow_shutdown']:
      Subprocess.run(cmd)
      self.halt()

  def _is_control_program(self):
    return self.echomesh.config['control_program']

def router(echomesh, clients):
  def _error(data):
    LOGGER.error("Didn't understand command '%s'", data['type'])

  r = Router(echomesh, clients)
  return lambda data: getattr(r, data['type'], _error)(data)
