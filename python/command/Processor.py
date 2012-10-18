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
  'help',
  'list',
)

def _usage():
  print('Commands are', ', '.join(SIMPLE_COMMANDS + REMAINING_COMMANDS))

def process(command, echomesh):
  if command in SIMPLE_COMMANDS:
    echomesh.discovery.send(dict(type=command))

  elif command == 'discover':
    print("Command '%s' not implemented" % command)
    _usage()

  elif command == 'help':
    _usage()

  elif command == 'list':
    for client in echomesh.clients.get_clients().itervalues():
      print(client)

  elif command == 'quit':
    return False

  elif command:
    print("Didn't understand command '%s'" % command)
    _usage()

  return True

