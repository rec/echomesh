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
  return os.path.join('nodes', node, filename)

def load_any(*filepath):
  for p in PATH:
    fp = join(p, filepath)
    if os.path.exists(fp):
      return fp

def load_all(*filepath):
  return [File.yaml_load(join(p, *filepath)) for p in PATH]
