from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import subprocess
import traceback

from echomesh.util import Log
from echomesh.util import Platform
from echomesh.util import Subprocess

LOGGER = Log.logger(__name__)

GIT_BINARY = Platform.IS_MAC and '/usr/local/git/bin/git' or '/usr/bin/git'
GIT_LOG = ['log', '-n1', '--abbrev=40']
GIT_DIRECTORY = '.'

def run_git_command(command, config=None, cwd=None, log_commands=False):
  binary = GIT_BINARY
  if config and ('git_binary' in config['git']):
    binary = config['git']['binary']
  cwd = cwd or GIT_DIRECTORY
  assert not log_commands
  if log_commands:
    LOGGER.info(' '.join(['git'] + list(command)))
  return Subprocess.run([binary] + list(command), cwd=cwd)

def run_git_commands(log_commands, *commands):
  for c in commands:
    try:
      lines, returncode = run_git_command(c, log=log_commands)
      if log_commands or returncode:
        for line in lines:
          LOGGER.info(line)
      if returncode:
        return False

    except:
      LOGGER.critical(traceback.format_exc())
      LOGGER.error('git command failed')
      return False

  return True
