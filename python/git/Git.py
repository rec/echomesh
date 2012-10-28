from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

from util import Platform
from util import Subprocess

GIT_BINARY = Platform.IS_MAC and '/usr/local/git/bin/git' or '/usr/bin/git'
GIT_LOG = ['log', '-n1', '--abbrev=40']

def run_git_command(command, config=None, cwd=None):
  binary = GIT_BINARY
  if config and 'git_binary' in config['git']:
    binary = config['git']['binary']
  return Subprocess.run([binary] + command, cwd=cwd).splitlines()

def most_recent_commit(config=None, cwd=None):
  lines = run_git_command(GIT_LOG, config)
  return lines[0].split()[1], lines[-1].strip()
