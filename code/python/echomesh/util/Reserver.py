from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import threading

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
    self.reserved = collections.defaultdict(lambda: 0)
    self.reserved_uniquely = set()
    self.lock = lock or threading.Lock()

  def reserve(self, items):
    with self.lock:
      res = self.reserved_uniquely.intersection(items)
      if res:
        raise Exception('%s are already uniquely reserved.' % ', '.join(res))
      for item in items:
        self.reserved[item] += 1

  def reserve_uniquely(self, *items):
    with self.lock:
      res = [i for i in items if self.reserved[i]]
      if res:
        raise Exception('%s are already reserved.' % ', '.join(res))
      for item in items:
        self.reserved[item] += 1
      self.reserved_uniquely.update(items)

  def release(self, *items):
    with self.lock:
      not_reserved = []
      for item in items:
        count = self.reserved[item]
        if count <= 1:
          if count < 1:
            not_reserved.append(item)
          del self.reserved[item]
        else:
          self.reserved[item] = count - 1

      self.reserved_uniquely.difference_update(items)
