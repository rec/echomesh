import copy
import os
import threading
import time

from echomesh.network import Address

from echomesh.util import Locker
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Clients(object):
  TYPE = 'client'

  def __init__(self, echomesh):
    self.lock = threading.RLock()
    self.echomesh = echomesh
    self.type = Clients.TYPE
    source = Address.NODENAME
    self.data = dict(type=self.type,
                     time=time.time(),
                     source=source,
                     mac_address=Address.MAC_ADDRESS,
                     ip_address=Address.IP_ADDRESS)

    self._clients = {source: self.data}

  def _send(self):
    self.echomesh.send(**self.data)

  def start(self):
    self._send()

  def new_client(self, data):
    with Locker.Locker(self.lock):
      source = data['source']
      client = self._clients.get(source, None)
      if client != data:
        self._clients[source] = data
        if client != self.data:
          LOGGER.info('New client %s', source)
          self._send()

  def getclients(self):
    with Locker.Locker(self.lock):
      return copy.deepcopy(self._clients)
