from __future__ import absolute_import, division, print_function, unicode_literals

import os

from echomesh.base import Platform
from echomesh.build.BuildConfig import CONFIG

_DARWIN_COMMAND = ('xcodebuild -project Builds/MacOSX/echomesh.xcodeproj '
                   '-configuration {Config}')

COMMANDS = {
  'library': {
    'darwin': _DARWIN_COMMAND
    },
  'clean': {
    'darwin': '%s clean' % _DARWIN_COMMAND
    },
}

def execute(command):
  config = 'debug' if CONFIG.debug else 'release'
  command = command.format(config=config, Config=config.capitalize())
  if CONFIG.verbose:
    print('$ %s' % command)
  result = os.system(command)
  if result:
    raise Exception('%s\n failed with code %s' % (command, result))

def execute_command(cmd):
  cmd_dict = COMMANDS[cmd]
  command = cmd_dict.get(Platform.PLATFORM)
  if command:
    execute(command)
  else:
    raise Exception('No %s command for platform %s.' % (cmd, Platform.PLATFORM))

