from __future__ import absolute_import, division, print_function, unicode_literals

import time

from config import Config
from git import Git
from util import File
from util import Log

LOGGER = Log.logger(__name__)

# TODO: these are a subset the methods of Router, so we need
# this information in two places... deal with that!
REMOTE_COMMANDS = (
  'clear',
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
  'commit',
  'help',
  'list',
  'quit',
)

ALL_COMMANDS = REMOTE_COMMANDS + FILE_COMMANDS + SIMPLE_COMMANDS

_UPDATE_GIT = (
  ('add', 'config/config.yml'),
  ('commit', '-m', '"Automatic checkin of config file"'),
  #  ('push', 'origin', 'master'),
  )

def _usage():
  LOGGER.error('Commands are %s', ', '.join(ALL_COMMANDS))

def _play(filename):
  from sound import FilePlayer

  FilePlayer.FilePlayer(filename).start()
  time.sleep(2)
  FilePlayer.FilePlayer(filename, level=0.5).start()

  time.sleep(2)
  FilePlayer.FilePlayer(filename, pan=1.0).start()

  time.sleep(2)
  pan = [[0, -1], [1, 1], [2, -1], [3, 1], [4, -1]]
  FilePlayer.FilePlayer(filename, pan=pan).start()

def _config(filename=Config.CONFIG_FILE):
  config = File.yaml_load_all(filename)
  if config:
    echomesh.send(type='config', data=config)
  else:
    LOGGER.error("Didn't get any data from file %s", filename)

def _file_command(echomesh, cmd, *args):
  if cmd == 'play':
    if args:
      _play(args)
    else:
      LOGGER.error('play needs a file argument' % cmd)

  else:
    _config(*args)

def _simple_command(echomesh, cmd):
  if cmd == 'quit':
    LOGGER.info('quitting')
    return False

  elif cmd == 'help':
    _usage()

  elif cmd == 'list':
    for client in echomesh.clients.get_clients().itervalues():
      LOGGER.info(client)

  elif cmd == 'commit':
    LOGGER.info('Committing changes to the configuration')
    if Git.run_git_commands(*_UPDATE_GIT):
      LOGGER.info('Changes committed')
    else:
      LOGGER.info('Changes were NOT committed')

  return True

def process(command, echomesh):
  parts = command.strip().split(' ')
  if not parts:
    return

  cmd = parts[0]
  if cmd in REMOTE_COMMANDS:
    echomesh.send(type=command)

  elif cmd in FILE_COMMANDS:
    if len(parts) <= 2:
      _file_command(echomesh, *parts)
    else:
      LOGGER.error('Command %s has too many arguments' % cmd)

  elif cmd in SIMPLE_COMMANDS:
    return _simple_command(echomesh, cmd)

  else:
    LOGGER.error("Didn't understand command '%s'", cmd)
    _usage()

  return True
