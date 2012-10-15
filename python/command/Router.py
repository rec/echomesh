from __future__ import absolute_import, division, print_function, unicode_literals

from config import Config
from util import Subprocess

SHUTDOWN = ['/sbin/shutdown', '-h', 'now']
RESTART = ['/sbin/shutdown', '-r', 'now']

def _start(data):
  print('Starting');

def _quit(data):
  print('Quitting');

def router(config, clients):
  return {
    clients.type: clients.new_client,
    'config': Config.change,
    'quit': _quit,
    'restart': lambda d: Subprocess.run(RESTART),
    'shutdown': lambda d: Subprocess.run(SHUTDOWN),
    'start': _start,
    }
