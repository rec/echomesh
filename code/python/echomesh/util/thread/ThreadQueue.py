from __future__ import absolute_import, division, print_function, unicode_literals

from six.moves import queue

from echomesh.util.thread import ThreadLoop

DEFAULT_TIMEOUT = 0.5

class ThreadQueue(ThreadLoop.ThreadLoop):
  def __init__(self):
    super(ThreadQueue, self).__init__()
    self._queue = queue.Queue()

  def queue_items(self):
    while self.is_running:
      try:
        yield self._queue.get(timeout=DEFAULT_TIMEOUT)
      except queue.Empty:
        pass


