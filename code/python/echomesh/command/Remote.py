from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Registry

def remote(name):
  return lambda echomesh: echomesh.send(type=name)

COMMANDS = [
  ('halt', 'Quit all the remote echomesh nodes.'),
  ('restart', 'Restart the echomesh programs on all the remote nodes.'),
  ('shutdown', 'Shutdown all the remote nodes.'),
  ('update', 'Update all the remote nodes from git, then restart them.')
  ]

for command, help_text in COMMANDS:
  Registry.register(command, remote(command), help_text)

def broadcast(on_or_off=None):
  pass

