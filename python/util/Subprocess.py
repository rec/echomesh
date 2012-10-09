from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

def run(command):
  popen = subprocess.Popen(command, stdout=subprocess.PIPE)
  popen.wait()
  return popen.stdout.read()

