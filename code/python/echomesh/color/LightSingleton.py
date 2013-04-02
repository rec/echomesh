from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.base import Config
from echomesh.util import Log
from echomesh.util import Importer

LOGGER = Log.logger(__name__)

_TYPE_MAP = {'spi': 'echomesh.light.SPILightBank'}

class LightSingleton(object):
  def __init__(self):
    self.light_bank = None
    self.lock = threading.Lock()

  def add_client(self, client):
    with self.lock:
      if not self.light_bank:
        self.light_bank = Importer.imp(_TYPE_MAP[Config.get('light', 'type')])()
      self.light_bank.add_client(client)

  def remove_client(self, client):
    with self.lock:
      if not self.light_bank.add_client(client):
        self.light_bank = None

SINGLETON = LightSingleton()
