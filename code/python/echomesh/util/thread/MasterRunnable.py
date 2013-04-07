from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.thread.LockedList import LockedList
from echomesh.util.thread.Runnable import Runnable

LOGGER = Log.logger(__name__)

class MasterRunnable(Runnable):
  def __init__(self):
    super(MasterRunnable, self).__init__()
    self.runnables = LockedList()
    self.pausables = LockedList()
    self.joinables = LockedList()

  def add_slave(self, *slaves):
    self.runnables.add(*slaves)
    self.pausables.add(*slaves)
    self.joinables.add(*slaves)

  def add_pause_only_slave(self, *slaves):
    self.pausables.add(*slaves)
    self.joinables.add(*slaves)

  def remove_slave(self, *slaves):
    self.runnables.remove(*slaves)
    self.pausables.remove(*slaves)
    self.joinables.remove(*slaves)

  def add_mutual_pause_slave(self, *clients):
    self.add_slave(*clients)
    for c in clients:
      if c:
        c.pausables.add(self)

  def run(self):
    was_running = self.is_running
    super(MasterRunnable, self).run()
    self.runnables.foreach('run')

  def pause(self):
    if self.is_running:
      self.is_running = False
      self.pausables.foreach('pause')
      self.is_running = True
    super(MasterRunnable, self).pause()

  def begin(self):
    super(MasterRunnable, self).begin()
    self.runnables.foreach('begin')
