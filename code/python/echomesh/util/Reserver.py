from __future__ import absolute_import, division, print_function, unicode_literals

import collections

from echomesh.util.thread import Lock
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Reserver(object):
  """
  Reserve or uniquely reserve items from a set of items.

  If an item is already uniquely reserved, you can't reserve it at all.
  If an item is only reserved, then you can't uniquely reserve it, but you can
  reserve it.
  """
  def __init__(self, lock=None):
    self._reserved = collections.defaultdict(lambda: 0)
    self._reserved_uniquely = set()
    self.lock = lock or Lock.Lock()

  def reserved(self):
    with self.lock:
      return self._reserved.keys()

  def reserve(self, *items):
    with self.lock:
      res = self._reserved_uniquely.intersection(items)
      if res:
        print(res)
        raise Exception('%s are already uniquely reserved.' % res)
      for item in items:
        self._reserved[item] += 1

  def reserve_uniquely(self, *items):
    with self.lock:
      res = [i for i in items if self._reserved[i]]
      if res:
        raise Exception('%s are already reserved.' % res)
      for item in items:
        self._reserved[item] += 1
      self._reserved_uniquely.update(items)

  def unreserve(self, *items):
    with self.lock:
      not_reserved = []
      for item in items:
        count = self._reserved[item]
        if count <= 1:
          if count < 1:
            not_reserved.append(item)
          del self._reserved[item]
        else:
          self._reserved[item] = count - 1
      self._reserved_uniquely.difference_update(items)
    if not_reserved:
      LOGGER.warning("Some items were not reserved: %s", not_reserved)
