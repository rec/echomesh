from __future__ import absolute_import, division, print_function, unicode_literals

from six.moves import queue

from echomesh.util.thread.ThreadRunnable import ThreadRunnable
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class SocketThread(ThreadRunnable):
  def __init__(self, echomesh_socket, target, name):
    super(SocketThread, self).__init__(target=target)
    self.echomesh_socket = echomesh_socket
    self.socket = echomesh_socket.socket
    self.queue = queue.Queue()
    self.add_mutual_pause_slave(self._socket)
    self.name = name
    self.buffer = ''

  def receive(self, packet):
    self.buffer += data
    parts = self.buffer.split(SEGMENT)
    self.buffer = parts.pop()
    for part in parts:
      if part:
        try:
          yaml_part = yaml.safe_dump(part)
        except:
          LOGGER.error("Didn't understand incoming part %s", part, exc_info=1)
        else:
          self.queue.put(yaml_part)

class SocketQueue(object):
  def __init__(self, echomesh_socket, queue):
    self.socket = echomesh_socket.socket
    self.queue = queue.Queue()
    self.buffer = ''
    self.pause = echomesh_socket.pause
    self.join = echomesh_socket.join

  def receive(self, packet):
    self.buffer += data
    parts = self.buffer.split(SEGMENT)
    self.buffer = parts.pop()
    for part in parts:
      if part:
        try:
          yaml_part = yaml.safe_dump(part)
        except:
          LOGGER.error("Didn't understand incoming packet %s", part, exc_info=1)
        else:
          if yaml_part:
            self.queue.put(yaml_part)
