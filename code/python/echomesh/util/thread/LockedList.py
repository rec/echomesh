from __future__ import absolute_import, division, print_function, unicode_literals

from threading import Lock
from echomesh.util import Log

LOGGER = Log.logger(__name__)

RAISE_EXCEPTIONS = True

class LockedList(object):
  def __init__(self):
    self._entries = []
    self._lock = Lock()

  def entries(self):
    with self._lock:
      return self._entries[:]

  def foreach(self, member_name):
    for e in self.entries():
      try:
        getattr(e, member_name)()
      except:
        LOGGER.error('%s:%s', member_name, e)
        if RAISE_EXCEPTIONS:
          raise

  def clear(self):
    with self._lock:
      self._entries[:] = []

  def add(self, *entries):
    with self._lock:
      for e in entries:
        if e and e not in self._entries:
          self._entries.append(e)

  def add_to(self, *entries):
    for e in entries:
      if e:
        e.add(self)

  def remove(self, *entries):
    with self._lock:
      for e in entries:
        try:
          self._entries.remove(e)
        except ValueError:
          LOGGER.warn('Tried to remove non-existent value %s from %s',
                      e, self._entries)
