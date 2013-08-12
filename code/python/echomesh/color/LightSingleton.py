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
  'client': 'echomesh.color.ExternalLightBank',
  'tk': 'echomesh.color.TkLightBank',
  'spi': 'echomesh.color.SpiLightBank'
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
    with self.lock:
      self._make_lights()
      self.lights.add_client(client)

  def remove_client(self, client):
    with self.lock:
      if self.lights:
        self.lights.remove_client(client)
      self._stop_lights()

  def _make_lights(self):
    if not self.lights:
      classpath = _TYPE_MAP[Config.get('light', 'visualizer', 'type')]
      self.lights = Importer.imp(classpath, defer_failure=False)()
      self.lights.start()

  def _stop_lights(self):
    if self.lights and not (self.lights.has_clients() or self.owner_count > 0):
      self.lights.pause()
      self.lights = None

_SINGLETON = LightSingleton()
add_client = _SINGLETON.add_client
remove_client = _SINGLETON.remove_client
add_owner = _SINGLETON.add_owner
remove_owner = _SINGLETON.remove_owner
stop = _SINGLETON.pause
