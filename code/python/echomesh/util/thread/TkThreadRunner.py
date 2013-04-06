from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import Queue

_QUEUE = None
_LOCK = threading.Lock()
MAIN_THREAD = threading.current_thread()

def defer(item):
  with _LOCK:
    global _QUEUE
    if _QUEUE:
      _QUEUE.put(item)

def run():
  with _LOCK:
    global _QUEUE
    if not _QUEUE:
      _QUEUE = Queue.Queue()

def stop():
  with _LOCK:
    global _QUEUE
    if _QUEUE:
      _QUEUE = None

def execute_queue(timeout=None):
  assert threading.current_thread() is MAIN_THREAD
  while _QUEUE:
    try:
      _QUEUE.get(False, timeout)()
      if timeout is not None:
        return
    except Queue.Empty:
      return
