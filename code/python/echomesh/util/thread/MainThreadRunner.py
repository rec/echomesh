from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import Queue

_QUEUE = Queue.Queue()
run_on_main_thread = _QUEUE.put

_THREAD = threading.current_thread()
_RUN_EVERY_TIME = None

def run_one(timeout=None):
  assert threading.current_thread() is _THREAD
  if _RUN_EVERY_TIME:
    _RUN_EVERY_TIME()
  while True:
    try:
      _QUEUE.get(timeout is not None, timeout)()
      if timeout is not None:
        return
    except Queue.Empty:
      return

def run_every_time(function):
  global _RUN_EVERY_TIME
  _RUN_EVERY_TIME = function

