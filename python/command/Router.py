from __future__ import absolute_import, division, print_function, unicode_literals

from config import Config
from util import Subprocess

SHUTDOWN = ['/sbin/shutdown', '-h', 'now']
RESTART = ['/sbin/shutdown', '-r', 'now']

class Router(object):
  def __init__(self, echomesh)
    self.echomesh = echomesh

  def close(self, data):
    print('Quitting');
    self.echomesh.close()

  def shutdown(self, data):
    self.close()
    print('Shutting down')
    Subprocess.run(SHUTDOWN)

  def shutdown(self, data):
    self.close()
    print('Restarting')
    Subprocess.run(SHUTDOWN)

def router(echomesh, config, clients):
  r = Router(echomesh)
  return {
    clients.type: clients.new_client,
    'config': Config.change,
    'quit': r.close,
    'restart': r.restart,
    'shutdown': r.shutdown,
    }
