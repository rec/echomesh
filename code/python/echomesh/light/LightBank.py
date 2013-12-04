from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.base import Config
from echomesh.expression import UnitConfig
from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop
from echomesh.util.thread import Lock

LOGGER = Log.logger(__name__)

class LightBank(ThreadLoop):
  def __init__(self, is_daemon=True, name='LightBank'):
    super(LightBank, self).__init__(is_daemon=is_daemon, name=name)
    self.clients = set()
    self.lock = Lock.Lock(fake=True)
    self.loops = 0
    self.data = None

  def clear(self):
    pass

  def _before_thread_start(self):
    self._next_time = time.time()
    Config.add_client(self)

  def _after_thread_pause(self):
    self.clear()

  def pause(self):
    LOGGER.vdebug('LightBank.pause')
    super(LightBank, self).pause()

  def add_client(self, client):
    with self.lock:
      self.clients.add(client)
    LOGGER.vdebug('add_client %s', client)

  def remove_client(self, client):
    with self.lock:
      try:
        self.clients.remove(client)
      except KeyError:
        LOGGER.error('Removed client we didn\'t add %s', client)
        pass
    LOGGER.vdebug('remove_client %s', client)

  def has_clients(self):
    with self.lock:
      return not not self.clients

  def single_loop(self):
    with self.lock:
      client_lights = []
      failed_clients = set()
      for client in self.clients:
        try:
          client_lights.append(client.evaluate())

        except:
          LOGGER.error('in client %s', client)
          failed_clients.add(client)
      for c in failed_clients:
         self.clients.remove(c)

    if not client_lights:
      return

    self._fill_data(client_lights, UnitConfig.get('light', 'brightness'))
    if self.is_running:
      self._display_lights()
      LOGGER.vdebug('single_loop lights')

    if self.is_running:
      period = UnitConfig.get('light', 'visualizer', 'period')
      self._next_time += period
      # TODO: which period?
      sleep_time = max(0, self._next_time - time.time())
      if sleep_time:
        time.sleep(sleep_time)

  def config_update(self, get):
    self.count = get('light', 'count')
    self.data = self._make_data(self.count)

  def _make_data(self, count):
    pass

  def _fill_data(self, client_lights, brightness):
    pass

  def _display_lights(self):
    pass
