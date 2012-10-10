from __future__ import absolute_import, division, print_function, unicode_literals

from util import Subprocess

SHUTDOWN = ['/sbin/shutdown', '-h', 'now']
RESTART = ['/sbin/shutdown', '-r', 'now']

def _start():
  print('Starting');

def _quit():
  print('Quitting');


ROUTER = dict(
  quit=_quit,
  restart=lambda: Subprocess.run(RESTART),
  shutdown=lambda: Subprocess.run(SHUTDOWN),
  start=_start)
