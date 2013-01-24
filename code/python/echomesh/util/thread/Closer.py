from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.thread.LockedList import LockedList
from echomesh.util.thread import Openable

LOGGER = Log.logger(__name__)

class Closer(Openable.Openable):
  def __init__(self):
    super(Closer, self).__init__()
    self.openables = LockedList()
    self.closeables = LockedList()

  def add_slave(self, *slaves):
    self.openables.add(*slaves)
    self.closeables.add(*slaves)

  def remove_slave(self, *slaves):
    self.openables.remove(*slaves)
    self.closeables.remove(*slaves)

  def add_slave_closer(self, *clients):
    self.add_slave(*clients)
    for c in clients:
      c and c.closeables.add(self)

  def start(self):
    super(Closer, self).start()
    self.openables.foreach(lambda e: e.start())

  def close(self):
    if self.is_running:
      super(Closer, self).close()
      self.closeables.foreach(lambda e: e.close())

  def join(self):
    super(Closer, self).join()
    self.openables.foreach(lambda e: e.join())

class _ExitCloser(Closer):
  pass

EXIT_CLOSER = _ExitCloser()

def close_on_exit(to_close):
  EXIT_CLOSER.add_slave(to_close)

def on_exit():
  EXIT_CLOSER.close()
