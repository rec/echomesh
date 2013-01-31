from __future__ import absolute_import, division, print_function, unicode_literals

# Send and receive UDP broadcast packets

import select
import socket
import sys
import time

from echomesh.base import Platform
from echomesh.util.thread.MasterRunnable import MasterRunnable

DEFAULT_PORT = 1248
DEFAULT_BUFFER_SIZE = 1024

USAGE = '%s read | write' % sys.argv[0]

class Socket(MasterRunnable):
  def __init__(self, port):
    super(Socket, self).__init__()
    self.port = port
    self.bind_port = 0
    self.socket = None

  def _on_start(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.bind(('', self.bind_port))

  def _on_stop(self):
    self.socket.close()
    self.socket = None

class Send(Socket):
  def _on_start(self):
    super(Send, self)._on_start()
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  def write(self, data):
    try:
      self.socket.sendto(data, ('<broadcast>', self.port))
    except:
      if self.is_running:
        raise

class Receive(Socket):
  def __init__(self, port, buffer_size=DEFAULT_BUFFER_SIZE):
    super(Receive, self).__init__(port)
    self.bind_port = port
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

