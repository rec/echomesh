from __future__ import absolute_import, division, print_function, unicode_literals

from util import Log

SIMPLE_COMMANDS = (
  'halt',
  'rerun',
  'restart',
  'restart',
  'shutdown',
  'start',
  'stop',
  )

REMAINING_COMMANDS = (
  'discover',
  'help',
  'list',
)

def process(command, echomesh):
  if command in SIMPLE_COMMANDS:
    echomesh.discovery.send(dict(type=command))

  elif command == 'discover':
    pass

  elif command == 'help':
    print('Commands are', ', '.join(SIMPLE_COMMANDS + REMAINING_COMMANDS))

  elif command == 'list':
    pass

  elif command == 'quit':
    return False

  elif command:
    Log.logger(__name__).error("Didn't understand command '%s'" % command)

  return True

