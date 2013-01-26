from __future__ import absolute_import, division, print_function, unicode_literals

from threading import Lock
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class LockedList(object):
  def __init__(self):
    self._entries = []
    self._lock = Lock()

  def entries(self):
    with self._lock:
      return self._entries[:]

  def foreach(self, function):
    for e in self.entries():
      try:
        function(e)
      except:
        LOGGER.error("Couldn't %s on %s", function, e)
        raise

  def clear(self):
    with self._lock:
      self._entries.clear()

  def add(self, *entries):
    with self._lock:
      for e in entries:
        if e and e not in self._entries:
          self._entries.append(e)

  def add_to(self, *entries):
    for e in entries:
      e and e.add(self)

  def remove(self, *entries):
    with self._lock:
      for e in entries:
        try:
          self._entries.remove(e)
        except ValueError:
          LOGGER.error('Tried to remove non-existent value %s from %s',
                       e, self._entries)
