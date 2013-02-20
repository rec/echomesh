from __future__ import absolute_import, division, print_function, unicode_literals

from six.moves import queue

from echomesh.util.thread.ThreadRunnable import ThreadRunnable

class SocketThread(ThreadRunnable):
  def __init__(self, socket, target):
    super(SocketThread, self).__init__(target=target)
    self.socket = socket
    self.queue = queue.Queue()
    self.add_mutual_stop_slave(self.socket)

