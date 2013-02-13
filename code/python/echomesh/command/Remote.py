from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Registry

def remote(name):
  return lambda echomesh: echomesh.send(type=name)

COMMANDS = ['clear', 'halt', 'refresh', 'rerun', 'restart', 'shutdown',
            'update']

for command in COMMANDS:
  Registry.register(command, remote(command))
