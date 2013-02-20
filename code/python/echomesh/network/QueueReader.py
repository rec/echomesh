from __future__ import absolute_import, division, print_function, unicode_literals

from six.moves import queue

class QueueReader(object):
  def __init__(self, queue, runnable, timeout):
    self.queue = queue
    self.runnable = runnable
    self.timeout = timeout
    self.buffer = ''

  def read(self, buffer_size):
    if not self.buffer:
      while self.runnable.is_running:
        try:
          self.buffer = self.queue.get(self.timeout)
          break
        except queue.Empty:
          continue

    if len(self.buffer) > buffer_size:
      result = self.buffer[0:buffer_size]
      self.buffer = self.buffer_size[buffer_size:]
    else:
      result, self.buffer = self.buffer, ''

    return result


