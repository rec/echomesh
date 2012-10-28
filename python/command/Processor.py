from __future__ import absolute_import, division, print_function, unicode_literals

import time

from util import Log
from sound import FilePlayer

LOGGER = Log.logger(__name__)

# TODO: these are a subset the methods of Router, so we need
# this information in two places... deal with that!
SIMPLE_COMMANDS = (
  'halt',
  'play',
  'refresh',
  'rerun',
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
    echomesh.send(dict(type=command))

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
    if False:
      FilePlayer.FilePlayer(filename).start()
      time.sleep(2)
      FilePlayer.FilePlayer(filename, level=0.5).start()

      time.sleep(2)
      FilePlayer.FilePlayer(filename, pan=1.0).start()

      time.sleep(2)
    pan = [[0, -1], [1, 1], [2, -1], [3, 1], [4, -1]]
    FilePlayer.FilePlayer(filename, pan=pan).start()

  elif command:
    print("Didn't understand command '%s'" % command)
    _usage()

  return True

