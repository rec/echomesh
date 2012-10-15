import copy
import os
import threading
import time

from network import Address
from network import Locker

class Clients(object):
  TYPE = 'client'

  def __init__(self, sender):
    self._clients = {}
    self.lock = threading.RLock()
    self.send = sender.send
    self.type = Clients.TYPE
    self.data = dict(type=self.type,
                     time=time.time(),
                     nodename=os.uname()[1],
                     mac_address=Address.mac_address(),
                     ip_address=Address.ip_address())
    self.send(self.data)


  def new_client(self, data):
    with Locker.Locker(self.lock):
      nodename = data['nodename']
      c = self._clients.get(nodename, None)
      if c != data:
        print('New client', data)
        self._clients[nodename] = data
        if c != self.data:
          self.send(self.data)
        else:
          print('self client')

  def get_clients(self):
    with Locker.Locker(self.lock):
      return copy.deepcopy(self._clients)
