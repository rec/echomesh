from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Register
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def remote(name):
  return lambda echomesh: echomesh.send(type=name)

COMMANDS = [
  ('halt', 'Quit all the remote echomesh nodes.'),
  ('restart', 'Restart the echomesh programs on all the remote nodes.'),
  ('shutdown', 'Shutdown all the remote nodes.'),
  ('update', 'Update all the remote nodes from git, then restart them.')
  ]

for command, help_text in COMMANDS:
  Register.register(remote(command), command, help_text)
