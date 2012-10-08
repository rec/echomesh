#!/usr/bin/python

# Send UDP broadcast packets

import socket
import sys
import time

def send_broadcast(config, msg=None):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind(('', 0))
  s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

  while 1:
    data = msg or (repr(time.time()) + '\n')
    s.sendto(data, ('<broadcast>', config.discovery_port))
    time.sleep(2)

if __name__ == '__main__':
  import Config
  send_broadcast(Config)
