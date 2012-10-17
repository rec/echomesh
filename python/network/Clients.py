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

  def __init__(self, sender):
    self._clients = {}
    self.lock = threading.RLock()
    self.send = sender.send
    self.type = Clients.TYPE
    self.data = dict(type=self.type,
                     time=time.time(),
                     nodename=Address.NODENAME,
                     mac_address=Address.MAC_ADDRESS,
                     ip_address=Address.IP_ADDRESS)
    self.send(self.data)

  def new_client(self, data):
    with Locker.Locker(self.lock):
      nodename = data['nodename']
      c = self._clients.get(nodename, None)
      if c != data:
        self._clients[nodename] = data
        if c != self.data:
          LOGGER.info('New client', data)
          self.send(self.data)
        else:
          LOGGER.info('self client')

  def get_clients(self):
    with Locker.Locker(self.lock):
      return copy.deepcopy(self._clients)
