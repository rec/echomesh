from __future__ import absolute_import, division, print_function, unicode_literals

from six.moves import queue

from echomesh.util.thread.ThreadRunnable import ThreadRunnable
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class SocketThread(ThreadRunnable):
  def __init__(self, socket, target, name):
    super(SocketThread, self).__init__(target=target)
    self.socket = socket
    self.queue = queue.Queue()
    self.add_mutual_stop_slave(self.socket)
    self.name = name

  def join(self):
    LOGGER.debug('starting to join %s', self.name)
    super(SocketThread, self).join()
    LOGGER.debug('ended join %s', self.name)

