from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.base import Config
from echomesh.color import Combiner
from echomesh.expression import Units
from echomesh.expression import UnitConfig
from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop
from echomesh.util.thread import Lock

class LightBank(ThreadLoop):
  def __init__(self, is_daemon=True):
    super(LightBank, self).__init__(is_daemon=is_daemon)
    self.clients = set()
    self.lock = Lock.Lock()
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

  def remove_client(self, client):
    with self.lock:
      try:
        self.clients.remove(client)
      except KeyError:
        pass

  def has_clients(self):
    return not not self.clients

  def single_loop(self):
    with self.lock:
      client_lights = [client() for client in self.clients]
      lights = Combiner.combine(Combiner.sup, *client_lights)
    if not lights:
      return  # TODO: this always happens the first time:  why?
    self._display_lights(lights, UnitConfig.get('light', 'brightness'))
    self._next_time += UnitConfig.get('light', 'period')
    time.sleep(max(0, self._next_time - time.time()))

  def _display_lights(self, lights):
    pass
