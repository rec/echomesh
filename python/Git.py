#!/usr/bin/python

import subprocess

import Platform

GIT_BINARY = Platform.IS_MAC and '/usr/local/git/bin/git' or '/usr/bin/git'
GIT_LOG = [GIT_BINARY, 'log', '-n1', '--abbrev=40']

def mostRecentCommit(config=None):
  command = GIT_LOG[:]
  if config and hasattr(config, 'gitBinary'):
    command[0] = config.gitBinary

  popen = subprocess.Popen(command, stdout=subprocess.PIPE)
  popen.wait()
  lines = popen.stdout.read().splitlines()
  return lines[0].split()[1], lines[-1].strip()

