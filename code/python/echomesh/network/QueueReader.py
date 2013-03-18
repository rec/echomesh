from __future__ import absolute_import, division, print_function, unicode_literals

from six.moves import queue

FILE = open('/tmp/queue.txt', 'w')

class QueueReader(object):
  def __init__(self, _queue, runnable, timeout):
    self.queue = _queue
    self.runnable = runnable
    self.timeout = timeout
    self.buffer = ''

  def read(self, buffer_size):
    items, length = [self.buffer], len(self.buffer)
    while length < buffer_size and self.runnable.is_running:
      try:
        item = self.queue.get(block=not length, timeout=self.timeout)
        length += len(item)
        items.append(item)
      except queue.Empty:
        if length:  # We got something so we can quit.
          break
        else:
          continue

    if not self.runnable.is_running:
      return

    if length > buffer_size:
      last = items[-1]
      excess = length - buffer_size
      last_length = len(last) - excess
      self.buffer = last[last_length:]
      items[-1] = last[0:last_length]
    else:
      self.buffer = ''
    result = ''.join(items)
    FILE.write(result)
    return result
