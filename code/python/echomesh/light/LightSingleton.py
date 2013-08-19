from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.base import Config
from echomesh.util import Log
from echomesh.util import Importer
from echomesh.util.thread.Runnable import Runnable
from echomesh.util.thread import Lock

LOGGER = Log.logger(__name__)

MAIN_THREAD = threading.current_thread()

_TYPE_MAP = {
  'client': 'echomesh.light.ExternalLightBank',
  'spi': 'echomesh.light.SpiLightBank'
  }

class LightSingleton(Runnable):
  def __init__(self):
    super(LightSingleton, self).__init__()
    self.lights = None
    self.lock = Lock.Lock()
    self.owner_count = 0
    self.start()

  def _on_pause(self):
    if self.lights:
      self.lights.pause()
      self.lights = None

  def add_owner(self):
    self.owner_count += 1
    self._make_lights()

  def remove_owner(self):
    self.owner_count -= 1
    self._stop_lights()

  def add_client(self, client):
    self.lights.add_client(client)
    self._make_lights()

  def remove_client(self, client):
    with self.lock:
      if self.lights:
        self.lights.remove_client(client)
      self._stop_lights()

  def _make_lights(self):
    with self.lock:
      if self.lights:
        return
      classpath = _TYPE_MAP[Config.get('light', 'visualizer', 'type')]
      self.lights = Importer.imp(classpath, defer_failure=False)()
    self.lights.start()

  def _stop_lights(self):
    with self.lock:
      if not self.lights or self.lights.has_clients() or self.owner_count > 0:
        return
      lights, self.lights = self.lights, None
    lights.pause()

_SINGLETON = LightSingleton()
add_client = _SINGLETON.add_client
remove_client = _SINGLETON.remove_client
add_owner = _SINGLETON.add_owner
remove_owner = _SINGLETON.remove_owner
stop = _SINGLETON.pause
