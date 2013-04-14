from __future__ import absolute_import, division, print_function, unicode_literals

import threading
from six.moves import queue

from echomesh.util import Log
from echomesh.util.thread import Lock

LOGGER = Log.logger(__name__)

_QUEUE = None
_LOCK = Lock.Lock()
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
      _QUEUE = queue.Queue()

def stop():
  with _LOCK:
    global _QUEUE
    if _QUEUE:
      _QUEUE = None

def execute_queue(timeout=None):
  assert threading.current_thread() is MAIN_THREAD
  while _QUEUE:
    try:
      func = _QUEUE.get(False, timeout)
    except queue.Empty:
      return
    else:
      try:
        func()
      except:
        LOGGER.error()
      else:
        if timeout is None:
          continue
    return
