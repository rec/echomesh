from __future__ import absolute_import, division, print_function, unicode_literals

import six
import sys

from echomesh.base import Config
from echomesh.base import GetPrefix
from echomesh.expression import Units
from echomesh.util.thread import Lock

class _Client(object):
  def __init__(self):
    self.clients = {}
    self.lock = Lock.Lock()

  def get(self, *path):
    Config.add_client(self)
    with self.lock:
      value = self.clients.get(path)
      if not value:
        value = Units.convert(Config.get(*path))
        self.clients[path] = value
      return value

  def config_update(self, get):
    with self.lock:
      for path in six.iterkeys(self.clients):
        self.clients[path] = Units.convert(Config.get(*path))

_CLIENT = _Client()

get = _CLIENT.get
