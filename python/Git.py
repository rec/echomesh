#!/usr/bin/python

import subprocess

GIT_LOG = ['/usr/bin/git', 'log', '-n1', '--abbrev=40']

def mostRecentCommit(config=None):
  if config and hasattr(config, 'gitBinary'):
    GIT_LOG[0] = config.gitBinary

  popen = subprocess.Popen(GIT_LOG, stdout=subprocess.PIPE)
  popen.wait()
  lines = popen.stdout.read().splitlines()
  return lines[0].split()[1], lines[-1].strip()

