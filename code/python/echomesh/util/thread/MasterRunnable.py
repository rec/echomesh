from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.thread.LockedList import LockedList
from echomesh.util.thread.Runnable import Runnable

LOGGER = Log.logger(__name__)

class MasterRunnable(Runnable):
  def __init__(self):
    super(MasterRunnable, self).__init__()
    self.runnables = LockedList()
    self.stoppables = LockedList()
    self.joinables = LockedList()

  def add_slave(self, *slaves):
    self.runnables.add(*slaves)
    self.stoppables.add(*slaves)
    self.joinables.add(*slaves)

  def add_stop_only_slave(self, *slaves):
    self.stoppables.add(*slaves)
    self.joinables.add(*slaves)

  def remove_slave(self, *slaves):
    self.runnables.remove(*slaves)
    self.stoppables.remove(*slaves)
    self.joinables.remove(*slaves)

  def add_mutual_stop_slave(self, *clients):
    self.add_slave(*clients)
    for c in clients:
      c and c.stoppables.add(self)

  def start(self):
    if not self.is_running:
      super(MasterRunnable, self).start()
      ex = self.runnables.foreach(lambda e: e.start())
      if ex:
        LOGGER.error('Error%s during start:\n%s', ('s' if len(ex) > 1 else ''),
                     '   \n'.join(str(e) for e in ex))

  def stop(self):
    if self.is_running:
      self.is_running = False
      ex = self.stoppables.foreach(lambda e: e.stop())
      if ex:
        LOGGER.error('Errors during stop:\n%s', '\n'.join(str(e) for e in ex))
      super(MasterRunnable, self).stop()

  def join(self):
    super(MasterRunnable, self).join()
    self.runnables.foreach(lambda e: e.join())
