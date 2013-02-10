from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import CommandFile
from echomesh.base import Config
from echomesh.base import Yaml
from echomesh.base import Merge
from echomesh.util import Log
from echomesh.util import Subprocess

from gittwit.git import Git

LOGGER = Log.logger(__name__)

SUDO = '/usr/bin/sudo'
SHUTDOWN = '/sbin/shutdown'
SHUTDOWN_CMD = [SUDO, SHUTDOWN, '-h', 'now']
RESTART_CMD = [SUDO, SHUTDOWN, '-r', 'now']
GIT_UPDATE = ['pull', 'origin', 'master']

class Router(object):
  def __init__(self, echomesh, peers):
    self.echomesh = echomesh
    self.peers = peers
    Config.add_client(self)

  def config_update(self, get):
    self.control_program = get('control_program', 'enable')
    self.allow_shutdown = get('allow_shutdown')

  def clear(self, data):
    self.echomesh.remove_local()

  def peer(self, data):
    self.peers.new_peer(data)

  def config(self, msg):
    scope, new_config = msg['scope'], msg['config']
    f = CommandFile.config_file(scope)
    config = Merge.merge(Yaml.load(f), new_config, require_old_key=False)
    Yaml.dump_all(f, config)
    LOGGER.info('Changing configuration for %s', scope)

  def event(self, event):
    self.echomesh.receive_event(event)

  def halt(self, data):
    if not self.is_control_program:
      LOGGER.info('Quitting');
      self.echomesh.stop()

  def score(self, msg):
    score = msg.get('data')
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

  def stop(self, data):
    if not self.is_control_program:
      self.echomesh.stop()

  def _error(self, data):
    LOGGER.error("Command '%s' not implemented", data['type'])

  def _close_and_run(self, msg, cmd):
    LOGGER.info(msg)
    if self.allow_shutdown and not self.control_program:
      Subprocess.run(cmd)
      self.halt(cmd)

def router(echomesh, peers):
  def _error(data):
    LOGGER.error("Didn't understand command '%s'", data['type'])

  r = Router(echomesh, peers)
  return lambda data: getattr(r, data['type'], _error)(data)
