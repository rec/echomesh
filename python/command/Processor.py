from __future__ import absolute_import, division, print_function, unicode_literals

import time

from util import File
from util import Log
from sound import FilePlayer

LOGGER = Log.logger(__name__)

# TODO: these are a subset the methods of Router, so we need
# this information in two places... deal with that!
REMOTE_COMMANDS = (
  'halt',
  'refresh',
  'rerun',
  'restart',
  'shutdown',
  'start',
  'stop',
  'update',
  )

FILE_COMMANDS = (
  'config',
  'score',
  'play',
)

SIMPLE_COMMANDS = (
  'help',
  'list',
  'quit',
)

ALL_COMMANDS = REMOTE_COMMANDS + FILE_COMMANDS + SIMPLE_COMMANDS

def _usage():
  LOGGER.error('Commands are %s', ', '.join(ALL_COMMANDS))

def _play(filename):
  FilePlayer.FilePlayer(filename).start()
  time.sleep(2)
  FilePlayer.FilePlayer(filename, level=0.5).start()

  time.sleep(2)
  FilePlayer.FilePlayer(filename, pan=1.0).start()

  time.sleep(2)
  pan = [[0, -1], [1, 1], [2, -1], [3, 1], [4, -1]]
  FilePlayer.FilePlayer(filename, pan=pan).start()

def _file_command(echomesh, cmd, filename):
  if cmd == 'play':
    _play(filename)

  else:
    data = File.yaml_load_all(filename)
    if data:
      echomesh.send(type=cmd, data=data)
    else:
      LOGGER.error("Didn't get any data from file %s", filename)

def _simple_command(echomesh, cmd):
  if cmd == 'quit':
    LOGGER.info('quitting')
    return False

  elif cmd == 'help':
    _usage()

  elif cmd == 'list':
    for client in echomesh.clients.get_clients().itervalues():
      LOGGER.info(client)

  return True

def process(command, echomesh):
  parts = command.strip().split(' ')
  if not parts:
    return

  cmd = parts[0]
  if cmd in REMOTE_COMMANDS:
    echomesh.send(type=command)

  elif cmd in FILE_COMMANDS:
    if len(parts) is 2:
      _file_command(echomesh, cmd, parts[1])
    else:
      LOGGER.error('Command %s needs a file argument' % cmd)

  elif cmd in SIMPLE_COMMANDS:
    return _simple_command(echomesh, cmd)

  else:
    LOGGER.error("Didn't understand command '%s'", cmd)
    _usage()

  return True

