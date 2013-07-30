from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.base import Config
from echomesh.color import Combiner
from echomesh.expression import UnitConfig
from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop
from echomesh.util.thread import Lock

LOGGER = Log.logger(__name__)

class LightBank(ThreadLoop):
  def __init__(self, is_daemon=True):
    super(LightBank, self).__init__(is_daemon=is_daemon)
    self.clients = set()
    self.lock = Lock.Lock()
    self.loops = 0
    self.bytes = None

  def clear(self):
    pass

  def _before_thread_start(self):
    self._next_time = time.time()
    Config.add_client(self)

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
    with self.lock:
      return not not self.clients

  def single_loop(self):
    with self.lock:
      client_lights = []
      for client in self.clients:
        try:
          client_lights.append(client())
        except:
          LOGGER.error(limit=8)

    if not client_lights:
      return

    Combiner.combine_to_bytearray(self.bytes, client_lights,
                                  UnitConfig.get('light', 'brightness'))
    if self.is_running:
      self._display_lights()

    if self.is_running:
      self._next_time += UnitConfig.get('light', 'visualizer', 'period')
      # TODO: which period?
      time.sleep(max(0, self._next_time - time.time()))

  def config_update(self, get):
    self.count = get('light', 'count')
    self.bytes = bytearray(3 * self.count)

  def _display_lights(self):
    pass
