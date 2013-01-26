from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os
import threading
import time

from echomesh.base import Name

from threading import Lock
from echomesh.util.thread import Runnable
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Peers(Runnable.Runnable):
  TYPE = 'peer'

  def __init__(self, echomesh):
    super(Peers, self).__init__()
    self.lock = Lock()
    self.echomesh = echomesh
    self.type = Peers.TYPE
    source = Name.NAME
    self.data = dict(type=self.type,
                     time=time.time(),
                     source=source,
                     mac_address=Name.MAC_ADDRESS,
                     ip_address=Name.IP_ADDRESS)

    self._peers = {source: self.data}

  def _send(self):
    self.echomesh.send(**self.data)

  def start(self):
    super(Peers, self).start()
    self._send()

  def new_peer(self, data):
    with self.lock:
      source = data['source']
      peer = self._peers.get(source, None)
      if peer != data:
        self._peers[source] = data
        if peer != self.data:
          LOGGER.info('New peer %s', source)
          self._send()
          return True

  def get_peers(self):
    with self.lock:
      return copy.deepcopy(self._peers)
