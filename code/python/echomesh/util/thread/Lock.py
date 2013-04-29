from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import traceback

DEBUG = not True
SUSPICIOUS_LOCK = -1

def print_traceback():
  for line in traceback.format_stack():
    print(line.strip())

class _Locker(object):
  INDEX = 0

  def __init__(self, lock):
    self.lock = lock
    self.index = _Locker.INDEX
    _Locker.INDEX += 1
    print('--- Creating lock %d ---' % self.index)
    print_traceback()

  def __enter__(self):
    print('entering lock', self.index)
    if self.index == SUSPICIOUS_LOCK:
      print_traceback()
    self.lock.__enter__()
    print('entered lock', self.index)

  def __exit__(self, exc_type, exc_value, traceback):
    print('exiting lock', self.index)
    self.lock.__exit__(exc_type, exc_value, traceback)
    print('exited lock', self.index)

def Lock():
  lock = threading.Lock()
  return _Locker(lock) if DEBUG else lock

def RLock():
  lock = threading.RLock()
  return _Locker(lock) if DEBUG else lock
