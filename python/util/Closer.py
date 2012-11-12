from __future__ import absolute_import, division, print_function, unicode_literals

import weakref

from util import Log
from util.Openable import Openable

LOGGER = Log.logger(__name__)

class Closer(Openable):
  def __init__(self, *closers):
    super(Closer, self).__init__()
    try:
      self.closers = weakref.WeakSet(closers)
    except:
      self.closers = set()  # TODO: make sure this works in 2.6

  def add_closer(self, *closers):
    self.closers.update(closers)

  def mutual_closer(self, closer):
    self.add_closer(closer)
    closer.add_closer(self)

  def close_all(self):
    for c in self.closers:
      try:
        if c and c.is_open:
          c.close()
      except:
        LOGGER.error("Couldn't close %s" % repr(c))
    self.closers.clear()

  def close(self):
    super(Closer, self).close()
    self.close_all()

  def join(self):
    for c in self.closers:
      try:
        c.join()
      except:
        pass

