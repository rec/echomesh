#!/usr/bin/python

# Send and receive UDP broadcast packets

import select
import socket
import sys
import time

DEFAULT_PORT = 1248
DEFAULT_BUFFER_SIZE = 1024

USAGE = '%s read | write' % sys.argv[0]


class Socket(object):
  def __init__(self, port):
    self.port = port

  def __enter__(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.bind(('', self.bind_port))
    return self

  def __exit__(self, type, value, traceback):
    self.socket.close()


class SendSocket(Socket):
  def __init__(self, port):
    Socket.__init__(self, port)
    self.bind_port = 0

  def __enter__(self):
    Socket.__enter__(self)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    return self

  def send(self, data):
    self.socket.sendto(data, ('<broadcast>', self.port))


class ReceiveSocket(Socket):
  def __init__(self, port, buffer_size=DEFAULT_BUFFER_SIZE):
    Socket.__init__(self, port)
    self.bind_port = port
    self.buffer_size = buffer_size

  def __enter__(self):
    Socket.__enter__(self)
    self.socket.setblocking(0)
    return self

  def receive(self):
    result = select.select([self.socket],[],[])
    return result[0][0].recv(self.buffer_size)


if __name__ == '__main__':
  if len(sys.argv) is not 2:
    print USAGE
    exit(-1)

  elif sys.argv[1] == 'send':
    with SendSocket(DEFAULT_PORT) as ss:
      while True:
        ss.send(repr(time.time()) + '\n')
        time.sleep(2)

  elif sys.argv[1] == 'receive':
    with ReceiveSocket(DEFAULT_PORT) as rs:
      while True:
        print rs.receive()

  else:
    print USAGE
    exit(-1)
