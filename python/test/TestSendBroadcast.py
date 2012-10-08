#!/usr/bin/python

# Send UDP broadcast packets

import socket
import sys
import time

DEFAULT_PORT = 8888

def send_broadcast(port, msg=None):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind(('', 0))
  s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  while 1:
    data = msg or (repr(time.time()) + '\n')
    s.sendto(data, ('<broadcast>', port))
    time.sleep(2)

if __name__ == '__main__':
  send_broadcast(DEFAULT_PORT)
