from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import Queue

_QUEUE = Queue.Queue()
run_on_main_thread = _QUEUE.put

_THREAD = threading.current_thread()

def run_one(timeout=None):
  assert threading.current_thread() is _THREAD
  while True:
    try:
      _QUEUE.get(False, timeout)()
      if timeout is not None:
        return
    except Queue.Empty:
      return

