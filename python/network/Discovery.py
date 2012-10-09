from __future__ import absolute_import, division, print_function, unicode_literals

import os
import threading
import time
import yaml

from network import Address
from network import Broadcast
from network import Locker

DEFAULT_TIMEOUT = 0.2

class Discovery(object):
  def __init__(self, port, timeout):
    self.clients = {}
    self.port = port
    self.timeout = timeout

    self.lock = threading.RLock()
    self.data = yaml.dump(dict(time=time.time(),
                               nodename=os.uname()[1],
                               mac_address=Address.mac_address(),
                               ip_address=Address.ip_address()))
    self.is_running = True

    self.thread = threading.Thread(target=self.receive)
    self.thread.start()

  def close(self):
    self.is_running = False

  def send(self, data):
    with Broadcast.SendSocket(self.port) as ss:
      ss.send(data)

  def receive(self):
    with Broadcast.ReceiveSocket(self.port) as rs:
      self.send(self.data)
      while self.is_running:
        data = rs.receive(self.timeout)
        if data:
          self.receive_data(yaml.load(data))

  def receive_data(self, data):
    with Locker.Locker(self.lock):
      nodename = data['nodename']
      c = self.clients.get(nodename, None)
      if c and (c['time'] == data['time'] and
                c['nodename'] == data['nodename'] and
                c['ip_address'] == data['ip_address']):
        return
      print('New client', data)
      self.clients[nodename] = data
    self.send(self.data)

