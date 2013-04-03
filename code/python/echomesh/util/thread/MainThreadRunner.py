from __future__ import absolute_import, division, print_function, unicode_literals

import Queue

_QUEUE = Queue.Queue()

run_on_main_thread = _QUEUE.put

def run_one(timeout=None):
  while True:
    try:
      _QUEUE.get(timeout is not None, timeout)()
      if timeout is not None:
        return
    except Queue.Empty:
      return
