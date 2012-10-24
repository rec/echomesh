from __future__ import absolute_import, division, print_function, unicode_literals

import time

from util import Log
from sound import FilePlayer

LOGGER = Log.logger(__name__)

SIMPLE_COMMANDS = (
  'halt',
  'play',
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

  elif command.startswith('play'):
    # print('Command="%s"'  %command)
    filename = command.strip().split(' ')[1]
    print("playing", filename)
    FilePlayer.FilePlayer(filename).start()
    #time.sleep(3)
    #FilePlayer.FilePlayer(filename, level=1.0).start()

  elif command:
    print("Didn't understand command '%s'" % command)
    _usage()

  return True

