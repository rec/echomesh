from __future__ import absolute_import, division, print_function, unicode_literals

import os

from echomesh.network import Address
from echomesh.util import Platform
from echomesh.util.file import File

LEVELS = [
  '0.local',
  os.path.join('1.name', Address.NODENAME),
  os.path.join('2.platform', Platform.PLATFORM),
  '3.global',
  '4.default',
  ]

def expand(*path):
  # These first two lines are to make sure we split on / for Windows and others.
  filename = '/'.join(path)
  path = filename.split('/')
  return [os.path.join('command', i, *path) for i in LEVELS]

def resolve(*path):
  for f in expand(*path):
    if os.path.exists(f):
      return f
