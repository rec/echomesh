from __future__ import absolute_import, division, print_function, unicode_literals

try:
  from weakref import WeakSet

except:
  from weakrefset import WeakSet

from echomesh.base import Join
from echomesh.base import Reconfigure

_MERGE_CONFIG = None
_CLIENTS = WeakSet()
_NONE = object()
_ARGS = []

def reconfigure(args=None):
  global _ARGS, _MERGE_CONFIG
  if args:
    _ARGS = args
  _MERGE_CONFIG = Reconfigure.reconfigure(_ARGS)

def add_client(client):
  if not client in _CLIENTS:
    _CLIENTS.add(client)
    client.config_update(get)

def update_clients():
  for c in _CLIENTS:
    c.config_update(get)

def get_config():
  if not _MERGE_CONFIG:
    reconfigure()
  return _MERGE_CONFIG.config

def get(*parts):
  config = get_config()
  for part in parts:
    try:
      config = config[part]
    except KeyError:
      raise Exception('Couldn\'t find configuration "%s"' % '.'.join(parts))
    except AttributeError:
      raise Exception("Reached leaf configuration for %s: %s" %
                      ('.'.join(parts), config))
  return config

def assign(values):
  return _MERGE_CONFIG.assign(values)

# Automatically save any changed variables on exit.
def save(log=True):
  if get('autosave'):
    files = _MERGE_CONFIG.save()
    if log and files:
      print('Configuration automatically saved to', Join.join_file_names(files))
    return files

def assignments():
  return _MERGE_CONFIG.assignments()

def has_changes():
  return _MERGE_CONFIG.has_changes()

def get_changes():
  return _MERGE_CONFIG.get_changes()

