from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os
import threading
import time
import yaml

from network import Address
from network import Broadcast
from network import Locker

DEFAULT_TIMEOUT = 0.2
DISCOVERY_TYPE = 'discovery'

def _get_discovery_data(t=None):
  return dict(type=DISCOVERY_TYPE,
              time=t or time.time(),
              nodename=os.uname()[1],
              mac_address=Address.mac_address(),
              ip_address=Address.ip_address())

class Discovery(object):
  def __init__(self, port, timeout, callbacks):
    self.clients = {}
    self.port = port
    self.timeout = timeout

    self.callbacks = copy.deepcopy(callbacks)
    assert DISCOVERY_TYPE not in self.callbacks
    self.callbacks[DISCOVERY_TYPE] = self._receive_discovery

    self.lock = threading.RLock()
    self.discovery_data = yaml.dump(_get_discovery_data())
    self.is_running = True

    self.thread = threading.Thread(target=self._run_receive)
    self.thread.start()

  def close(self):
    self.is_running = False

  def send(self, data):
    with Broadcast.SendSocket(self.port) as ss:
      ss.send(data)

  def _run_receive(self):
    with Broadcast.ReceiveSocket(self.port) as rs:
      self.send(self.discovery_data)
      while self.is_running:
        data = rs.receive(self.timeout)
        if data:
          self._route(yaml.load(data))

  def _route(self, data):
    t = data.get('type', None)
    callback = self.callbacks.get(t, None)
    if callback:
      callback(data)
    else:
      print('No callbacks for type', type)

  def _receive_discovery(self, data):
    with Locker.Locker(self.lock):
      nodename = data['nodename']
      c = self.clients.get(nodename, None)
      if c and (c['time'] == data['time'] and
                c['nodename'] == data['nodename'] and
                c['ip_address'] == data['ip_address']):
        return
      print('New client', data)
      self.clients[nodename] = data
    self.send(self.discovery_data)

