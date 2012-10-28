import copy
import os
import threading
import time

from network import Address
from network import Locker
from util import Log

LOGGER = Log.logger(__name__)

class Clients(object):
  TYPE = 'client'

  def __init__(self, echomesh):
    self._clients = {}
    self.lock = threading.RLock()
    self.echomesh = echomesh
    self.type = Clients.TYPE
    self.data = dict(type=self.type,
                     time=time.time(),
                     source=Address.NODENAME,
                     mac_address=Address.MAC_ADDRESS,
                     ip_address=Address.IP_ADDRESS)

  def _send(self):
    self.echomesh.send(**self.data)

  def start(self):
    self._send()

  def new_client(self, data):
    with Locker.Locker(self.lock):
      source = data['source']
      c = self._clients.get(source, None)
      if c != data:
        self._clients[source] = data
        if c != self.data:
          LOGGER.info('New client %s', source)
          self._send()
        else:
          LOGGER.info('self client')

  def get_clients(self):
    with Locker.Locker(self.lock):
      return copy.deepcopy(self._clients)
