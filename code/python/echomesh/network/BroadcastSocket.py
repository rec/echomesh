from __future__ import absolute_import, division, print_function, unicode_literals

# Send and receive UDP broadcast packets

import select
import socket

SEND_FILE = open('/tmp/send.txt', 'w')

from echomesh.network import Socket

class BroadcastSocket(Socket.Socket):
  def __init__(self, port, bind_port):
    super(BroadcastSocket, self).__init__(
      port, bind_port, '', socket.SOCK_DGRAM)
    self.max_size = 1024

class Send(BroadcastSocket):
  def __init__(self, port):
    super(Send, self).__init__(port, 0)

  def _on_start(self):
    super(Send, self)._on_start()
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  def _raw_send(self, res):
    self.socket.sendto(res, ('<broadcast>', self.port))

  def old_write(self, data):
    try:
      while data:
        if len(data) <= self.max_size:
          res, data = data, ''
        else:
          res, data = data[0:self.max_size], data[self.max_size:]
        SEND_FILE.write(res)
        self._raw_send(res)
    except:
      if self.is_running:
        raise

class Receive(BroadcastSocket):
  def __init__(self, port):
    super(Receive, self).__init__(port, port)

  def _on_start(self):
    super(Receive, self)._on_start()
    self.socket.setblocking(0)

  def old_receive(self, timeout):
    try:
      result = select.select([self.socket], [], [], timeout)
      if result and result[0]:
        return result[0][0].recv(self.max_size)
    except:
      if self.is_running:
        raise
