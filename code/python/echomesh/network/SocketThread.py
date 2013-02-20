from __future__ import absolute_import, division, print_function, unicode_literals

from six.moves import queue

from echomesh.util.thread.ThreadRunnable import ThreadRunnable

def SocketThread(ThreadRunnable):
  def __init__(self, socket, target):
    super(SocketLoop, self).__init__(target=target)
    self.socket = socket
    self.queue = queue.Queue()
    self.add_mutual_stop_slave(self.socket)

  def iterator(self, timeout):
    while self.is_running:
      try:
        yield self.queue.get(timeout)
      except queue.Empty:
        pass

