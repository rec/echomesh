from __future__ import absolute_import, division, print_function, unicode_literals

import select
import socket

BUFFER_SIZE = 1024
DEFAULT_PORT = 1248
PORT_NAME = ''

## From http://code.activestate.com/recipes/577278/ (r1)

def receive_broadcast(port):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind((PORT_NAME, port))
  s.setblocking(0)

  while True:
    result = select.select([s],[],[])
    msg = result[0][0].recv(BUFFER_SIZE)
    yield msg

if __name__ == '__main__':
  for s in receive_broadcast(DEFAULT_PORT):
    print(s)
