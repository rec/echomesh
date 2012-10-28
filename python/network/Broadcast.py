from __future__ import absolute_import, division, print_function, unicode_literals

# Send and receive UDP broadcast packets

import select
import socket
import sys
import time
import traceback

from util.Openable import Openable
from util import Platform

DEFAULT_PORT = 1248
DEFAULT_BUFFER_SIZE = 1024

USAGE = '%s read | write' % sys.argv[0]

class Socket(Openable):
  def __init__(self, port):
    Openable.__init__(self)
    self.port = port
    self._open()

  def _open(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.bind(('', self.bind_port))

  def close(self):
    Openable.close(self)
    self.socket.close()

class SendSocket(Socket):
  def __init__(self, port):
    self.bind_port = 0
    Socket.__init__(self, port)

  def _open(self):
    Socket._open(self)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  def write(self, data):
    try:
      self.socket.sendto(data, ('<broadcast>', self.port))
    except:
      if self.is_open:
        raise


class ReceiveSocket(Socket):
  def __init__(self, port, buffer_size=DEFAULT_BUFFER_SIZE):
    self.bind_port = port
    self.buffer_size = buffer_size
    Socket.__init__(self, port)

  def _open(self):
    Socket._open(self)
    self.socket.setblocking(0)

  def receive(self, timeout):
    try:
      result = select.select([self.socket], [], [], timeout)
      return result[0] and result[0][0].recv(self.buffer_size)
    except select.error:
      if self.is_open:
        raise


class SocketReader(ReceiveSocket):
  def __init__(self, config, buffer_size=DEFAULT_BUFFER_SIZE):
    ReceiveSocket.__init__(self, config, buffer_size)
    self.unread = ''

  def read(self, buffer_size=0):
    while not self.unread:
      self.unread = self.receive()

    size = min(len(self.unread), buffer_size)

    result = self.unread[0: size]
    self.unread = self.unread[size:]
    return result

if __name__ == '__main__':
  if len(sys.argv) is not 2:
    print(USAGE)
    exit(-1)

  elif sys.argv[1] == 'send':
    with SendSocket(DEFAULT_PORT) as ss:
      while True:
        ss.send(repr(time.time()) + '\n')
        time.sleep(2)

  elif sys.argv[1] == 'receive':
    with ReceiveSocket(DEFAULT_PORT) as rs:
      while True:
        print(rs.receive())

  else:
    print(USAGE)
    exit(-1)

