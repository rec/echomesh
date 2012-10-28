from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

def run(command, **kwds):
  popen = subprocess.Popen(command, stdout=subprocess.PIPE, **kwds)
  popen.wait()
  return popen.stdout.read()

