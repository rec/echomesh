from __future__ import absolute_import, division, print_function, unicode_literals

# Send and receive UDP broadcast packets

import select
import socket

from echomesh.network import Socket

DEFAULT_BUFFER_SIZE = 65536

class Broadcast(Socket.Socket):
  def __init__(self, port, bind_port):
    super(Broadcast, self).__init__(port, bind_port, '', socket.SOCK_DGRAM)

class Send(Broadcast):
  def __init__(self, port):
    super(Send, self).__init__(port, 0)

  def _on_start(self):
    super(Send, self)._on_start()
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  def write(self, data):
    try:
      self.socket.sendto(data, ('<broadcast>', self.port))
    except:
      if self.is_running:
        raise

class Receive(Broadcast):
  def __init__(self, port, buffer_size=DEFAULT_BUFFER_SIZE):
    super(Receive, self).__init__(port, port)
    self.buffer_size = buffer_size

  def _on_start(self):
    super(Receive, self)._on_start()
    self.socket.setblocking(0)

  def receive(self, timeout):
    try:
      result = select.select([self.socket], [], [], timeout)
      return result[0] and result[0][0].recv(self.buffer_size)
    except:
      if self.is_running:
        raise

