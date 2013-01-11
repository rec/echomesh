from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util import Openable
from echomesh.util.thread import Locker

LOGGER = Log.logger(__name__)

class Closer(Openable.Openable):
  def __init__(self):
    super(Closer, self).__init__()
    self.closers = []
    self.lock = Locker.Lock()

  def add_closer(self, *closers):
    with Locker.Locker(self.lock):
      self.closers.extend(closers)

  def start_all(self):
    with Locker.Locker(self.lock):
      for closer in self.closers:
        closer.start()

  def mutual_closer(self, *closers):
    with Locker.Locker(self.lock):
      for closer in closers:
        self.add_closer(closer)
        closer.add_closer(self)

  def close_all(self):
    with Locker.Locker(self.lock):
      for c in list(self.closers):
        try:
          c and c.close()
        except:
          LOGGER.error("Couldn't close %s" % repr(c))
      self.closers = []

  def close(self):
    super(Closer, self).close()
    self.close_all()

  def join_all(self):
    with Locker.Locker(self.lock):
      for c in self.closers:
        try:
          c.join()
        except:
          pass

EXIT_CLOSER = Closer()

def close_on_exit(to_close):
  EXIT_CLOSER.add_closer(to_close)

def on_exit():
  EXIT_CLOSER.close()
