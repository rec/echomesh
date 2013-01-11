import copy
import os
import threading
import time

from echomesh.network import Address

from echomesh.util import Locker
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Peers(object):
  TYPE = 'peer'

  def __init__(self, echomesh):
    self.lock = threading.RLock()
    self.echomesh = echomesh
    self.type = Peers.TYPE
    source = Address.NODENAME
    self.data = dict(type=self.type,
                     time=time.time(),
                     source=source,
                     mac_address=Address.MAC_ADDRESS,
                     ip_address=Address.IP_ADDRESS)

    self._peers = {source: self.data}

  def _send(self):
    self.echomesh.send(**self.data)

  def start(self):
    self._send()

  def new_peer(self, data):
    with Locker.Locker(self.lock):
      source = data['source']
      peer = self._peers.get(source, None)
      if peer != data:
        self._peers[source] = data
        if peer != self.data:
          LOGGER.info('New peer %s', source)
          self._send()
          return True

  def get_peers(self):
    with Locker.Locker(self.lock):
      return copy.deepcopy(self._peers)
