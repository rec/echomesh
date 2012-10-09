from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

from util import Platform
from util import Subprocess

GIT_BINARY = Platform.IS_MAC and '/usr/local/git/bin/git' or '/usr/bin/git'
GIT_LOG = [GIT_BINARY, 'log', '-n1', '--abbrev=40']

def most_recent_commit(config=None):
  command = GIT_LOG[:]
  if config and hasattr(config, 'git_binary'):
    command[0] = config.git_binary

  lines = Subprocess.run(command).splitlines()
  return lines[0].split()[1], lines[-1].strip()
