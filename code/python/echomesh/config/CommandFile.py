import os

from echomesh.network import Address

from echomesh.util import Platform

LEVELS = [
  '0.local',
  os.path.join('1.name', Address.NODENAME),
  os.path.join('2.platform', Platform.PLATFORM),
  '3.global',
  '4.default',
  ]

def expand(filename):
  path = filename.split('/')
  return [os.path.join('command', i, *path) for i in LEVELS]

def resolve(filename):
  for f in expand(filename):
    if os.path.exists(f):
      return f

