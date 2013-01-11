from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.config import Config
from echomesh.network import Git
from echomesh.util import File
from echomesh.util import Log

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

def _usage(is_error=True):
  logger = LOGGER.error if is_error else LOGGER.info
  logger('Commands are %s', ', '.join(ALL_COMMANDS))

def _config(filename):
  # TODO: probably needs fixing.
  config = File.yaml_load_all(filename)
  if config:
    echomesh.send(type='config', data=config)
  else:
    LOGGER.error("Didn't get any data from file %s", filename)

def _file_command(echomesh, cmd, *args):
  if cmd == 'play':
    if args:
      from echomesh.sound.FilePlayer import FilePlayer
      FilePlayer.player(file=args[0])
    else:
      LOGGER.error('play needs a file argument' % cmd)

  else:
    _config(*args)

def _simple_command(echomesh, cmd):
  if cmd == 'quit':
    LOGGER.info('quitting')
    return False

  elif cmd == 'help':
    _usage(False)

  elif cmd == 'list':
    for peer in echomesh.peers.get_peers().itervalues():
      LOGGER.info(peer)

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

  elif cmd:
    LOGGER.error("Didn't understand command '%s'", cmd)
    _usage()

  return True
