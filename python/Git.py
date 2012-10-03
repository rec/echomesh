#!/usr/bin/python

import subprocess

GIT_LOG = ['/usr/bin/git', 'log', '-n1', '--decorate=full']

def mostRecentCommit():
  popen = subprocess.Popen(GIT_LOG, stdout=subprocess.PIPE)
  popen.wait()
  lines = popen.stdout.read().splitlines()
  return lines[0].split()[1], lines[4].strip()

