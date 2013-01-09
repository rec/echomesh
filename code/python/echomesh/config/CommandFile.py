import os

from echomesh.network import Address

from echomesh.util import File
from echomesh.util import Platform
from echomesh.util import Log

PATH = ['default',
        'global',
        os.path.join('name', Address.NODENAME),
        os.path.join('platform', Platform.PLATFORM),
        'local']

def join(node, filename):
  return os.path.join('command', node, filename.split('/'))

def resolve(filename):
  for p in PATH:
    fp = join(p, filename)
    if os.path.exists(fp):
      return fp

def load_all(filename):
  return [File.yaml_load(join(p, filename)) for p in PATH]
