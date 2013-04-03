from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.base import Config
from echomesh.util import Log
from echomesh.util import Importer

LOGGER = Log.logger(__name__)

_TYPE_MAP = {
  'tk': 'echomesh.color.TkLightBank',
  'spi': 'echomesh.color.SpiLightBank'}

class LightSingleton(object):
  def __init__(self):
    self.light_bank = None
    self.lock = threading.Lock()

  def add_client(self, client):
    with self.lock:
      if not self.light_bank:
        ltype = Config.get('light', 'type')
        classpath = _TYPE_MAP[ltype]
        self.light_bank = Importer.imp(classpath, defer_failure=False)()
      self.light_bank.add_client(client)

  def remove_client(self, client):
    with self.lock:
      if not self.light_bank.add_client(client):
        self.light_bank = None

_SINGLETON = LightSingleton()
add_client = _SINGLETON.add_client
remove_client = _SINGLETON.remove_client
