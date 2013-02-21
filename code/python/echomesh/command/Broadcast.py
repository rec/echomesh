from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Register
from echomesh.util import Log

LOGGER = Log.logger(__name__)

def broadcast(echomesh, on_or_off):
  on_or_off = on_or_off.lower()
  b_on = on_or_off in ['on', 'true']
  if not (b_on or on_or_off in ['off', 'false']):
    raise Exception('You can only turn broadcast mode "on" or "off".')
  name = 'ON' if b_on else 'off'
  if b_on == echomesh.broadcasting():
    message = 'was already'
  else:
    echomesh.set_broadcasting(b_on)
    message = 'is now'
  LOGGER.print('broadcast mode %s %s.', message, name)

BROADCAST_HELP = """
Set the broadcast mode on or off.

When broadcast mode is on, all start and stop commands are sent to all echomesh
nodes;  when broadcast mode is off, start and stop only go to this node.
"""

Register.register('broadcast', broadcast, BROADCAST_HELP)
