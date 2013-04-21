#!/usr/bin/env python

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from echomesh.base import Path
Path.fix_sys_path()

from echomesh.network.Server import Server

DEFAULT_ARGS = 'server localhost 1239 0.100'

def server(host, port, timeout):
  print('Starting server %s:%d' % (host, port))
  server = Server(host, port, timeout, True)
  server.start()
  parts = []

  while True:
    line = raw_input('%d: ' % len(parts))
    strip = line.strip()
    if strip and 'quit'.startswith(strip):
      return
    parts.append(line)
    if line.startswith('---'):
      server.write(''.join(parts))
      parts = []
      print('....sent!')

def client(host, port, timeout):
  pass

def relay():
  args = DEFAULT_ARGS.split()
  for i, arg in enumerate(sys.argv[1:]):
    args[i] = arg

  client_or_server, host, port, timeout = args
  if 'server'.startswith(client_or_server):
    server(host, int(port), float(timeout))
  else:
    client(host, int(port), float(timeout))

if __name__ == '__main__':
  relay()
