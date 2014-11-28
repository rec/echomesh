from __future__ import absolute_import, division, print_function, unicode_literals

import sys

from echomesh.base import Settings
from echomesh.base import GetPrefix
from echomesh.expression import Expression
from echomesh.util.thread import Lock

class _Client(object):
    def __init__(self):
        self.clients = {}
        self.lock = Lock.Lock()
        Settings.add_client(self)

    def get(self, *path):
        with self.lock:
            value = self.clients.get(path)
            if not value:
                value = Expression.convert(Settings.get(*path))
                self.clients[path] = value
            return value

    def settings_update(self, get):
        with self.lock:
            for path in self.clients.keys():
                self.clients[path] = Expression.convert(Settings.get(*path))

_CLIENT = _Client()

get = _CLIENT.get
