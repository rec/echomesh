from __future__ import absolute_import, division, print_function, unicode_literals

from config import Config
from util import Log
from util import Subprocess

SHUTDOWN = ['/sbin/shutdown', '-h', 'now']
RESTART = ['/sbin/shutdown', '-r', 'now']

LOGGER = Log.logger(__name__)

class Router(object):
  def __init__(self, echomesh, clients):
    self.echomesh = echomesh
    self.clients = clients

  def config(self, msg):
    config = msg.get('data', None)
    if data:
      echomesh.set_config(config)
    else:
      LOGGER.error('Empty config data received')

  def score(self, msg):
    score = msg.get('data', None)
    if score:
      echomesh.set_score(score)
    else:
      LOGGER.error('Empty score data received')
    self._error(data)

  def client(self, data):
    self.clients.new_client(data)

  def halt(self, data):
    if self._is_headless():
      LOGGER.info('Quitting');
      self.echomesh.close()

  def restart(self, data):
    self._close_and_run('Restarting', RESTART)

  def shutdown(self, data):
    self._close_and_run('Shutting down', SHUTDOWN)

  def event(self, event):
    self.echomesh.receive_event(event)

  # TODO!
  def rerun(self, data):
    self._error(data)

  def start(self, data):
    self._error(data)

  def stop(self, data):
    self._error(data)

  def refresh(self, data):
    self._error(data)

  def _error(self, data):
    LOGGER.error("Command '%s' not implemented", data['type'])

  def _close_and_run(self, msg, cmd):
    if self._is_headless() and self.config['allow_shutdown']:
      LOGGER.info(msg)
      Subprocess.run(cmd)
      self.halt()

  def _is_headless(self):
    return not self.echomesh.config['control_program']


def _error(data):
  LOGGER.error("Didn't understand command '%s'", data['type'])

def router(echomesh, clients):
  r = Router(echomesh, clients)
  return lambda data: getattr(r, data['type'], _error)(data)


