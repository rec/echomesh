from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import Queue

_QUEUE = None
_LOCK = threading.Lock()

def run(item=None):
  with _LOCK:
    global _QUEUE
    if not _QUEUE:
      _QUEUE = Queue.Queue()
    if item:
      _QUEUE.put(item)

def stop():
  with _LOCK:
    global _QUEUE
    if _QUEUE:
      _QUEUE = None

_THREAD = threading.current_thread()

def execute_queue(timeout=None):
  assert threading.current_thread() is _THREAD
  while _QUEUE:
    try:
      _QUEUE.get(False, timeout)()
      if timeout is not None:
        return
    except Queue.Empty:
      return

