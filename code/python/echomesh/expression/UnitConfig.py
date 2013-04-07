from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import sys

from echomesh.base import Config
from echomesh.base import GetPrefix
from echomesh.expression import Units

class _Client(object):
  def __init__(self):
    self.clients = {}
    self.lock = threading.Lock()
    Config.add_client(self.config_update)

  def get(self, *path):
    with self.lock:
      value = self.clients.get(path)
      if not value:
        value = Units.convert(Config.get(*path))
        self.clients[path] = value
      return value

  def config_update(self, get):
    with self.lock:
      for path in self.clients.iterkeys():
        self.clients[path] = get(*path)

_CLIENT = _Client()

get = _CLIENT.get
