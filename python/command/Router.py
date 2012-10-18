from __future__ import absolute_import, division, print_function, unicode_literals

from config import Config
from util import Log
from util import Subprocess

SHUTDOWN = ['/sbin/shutdown', '-h', 'now']
RESTART = ['/sbin/shutdown', '-r', 'now']

LOGGER = Log.logger(__name__)

class Router(object):
  def __init__(self, echomesh, config):
    self.echomesh = echomesh
    self.config = config

  def close(self, data):
    LOGGER.info('Quitting');
    self.echomesh.close()

  def restart(self, data):
    self._close_and_run('Restarting', RESTART)

  def shutdown(self, data):
    self._close_and_run('Shutting down', SHUTDOWN)

  def _close_and_run(self, msg, cmd):
    if self.config['allow_shutdown']:
      self.close()
      LOGGER.info(msg)
      Subprocess.run(cmd)


def router(echomesh, config, clients):
  r = Router(echomesh, config)
  return {
    clients.type: clients.new_client,
    'config': Config.change,
    'quit': r.close,
    'restart': r.restart,
    'shutdown': r.shutdown,
    }
