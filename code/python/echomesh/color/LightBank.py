from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time

from echomesh.base import Config
from echomesh.color import Combiner
from echomesh.expression import Units
from echomesh.expression import UnitConfig
from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop

class LightBank(ThreadLoop):
  def __init__(self, count=None):
    super(LightBank, self).__init__()
    self.count = Config.get('light', 'count') if count is None else count
    self.clients = set()
    self.lock = threading.Lock()
    self.period = Units.convert(Config.get('light', 'period'))
    self.loops = 0

  def clear(self):
    pass

  def _before_thread_start(self):
    self._next_time = time.time()

  def _after_thread_pause(self):
    self.clear()

  def add_client(self, client):
    with self.lock:
      self.clients.add(client)
    if not self.is_running:
      self.start()

  def remove_client(self, client):
    with self.lock:
      self.clients.remove(client)
      if self.clients:
        return True

  def single_loop(self):
    with self.lock:
      client_lights = [client() for client in self.clients]
      lights = Combiner.combine(Combiner.sup, *client_lights)
    self._display_lights(lights)
    self._next_time += self.period
    time.sleep(max(0, self._next_time - time.time()))

  def _display_lights(self, lights):
    pass
