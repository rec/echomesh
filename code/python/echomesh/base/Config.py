from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import six

from compatibility.weakref import WeakSet

from echomesh.base import Args
from echomesh.base import Join
from echomesh.base import Quit
from echomesh.base import Reconfigure

MERGE_CONFIG = None
_CLIENTS = WeakSet()
_NONE = object()

def reconfigure():
  global MERGE_CONFIG, CONFIGS_UNVISITED
  MERGE_CONFIG = Reconfigure.reconfigure()

def add_client(client):
  if not client in _CLIENTS:
    _CLIENTS.add(client)
    client.config_update(get)

def update_clients():
  for c in _CLIENTS:
    c.config_update(get)

def get(*parts):
  config = MERGE_CONFIG.config
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
  return MERGE_CONFIG.assign(values)

# Automatically save any changed variables on exit.
def save(log=True):
  if get('autosave'):
    files = MERGE_CONFIG.save()
    if log and files:
      print('Configuration automatically saved to', Join.join_file_names(files))

Quit.register_atexit(save)
