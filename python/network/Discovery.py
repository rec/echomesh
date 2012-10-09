#!/usr/bin/python

import os
import threading
import time
import yaml

from network import Broadcast
from network import Locker
from network import Address

class Discovery(object):
  def __init__(self, port):
    self.clients = {}
    self.port = port
    self.lock = threading.RLock()
    self.time = time.time()
    self.data = yaml.dump(dict(time=self.time,
                               nodename=os.uname()[1],
                               mac_address=Address.mac_address(),
                               ip_address=Address.ip_address()))

    self.thread = threading.Thread(target=self.receive)
    self.thread.start()

  def send(self):
    with Broadcast.SendSocket(self.port) as ss:
      ss.send(self.data)

  def receive(self):
    with Broadcast.ReceiveSocket(self.port) as rs:
      self.send()
      while True:
        data = rs.receive()
        if data:
          self.receive_data(yaml.load(data))
        else:
          return

  def receive_data(self, data):
    with Locker.Locker(self.lock):
      nodename = data['nodename']
      c = self.clients.get(nodename, None)
      if c and (c['time'] == data['time'] and
                c['nodename'] == data['nodename'] and
                c['ip_address'] == data['ip_address']):
        return
      print 'New client', data
      self.clients[nodename] = data
    self.send()


if __name__ == '__main__':
  discovery = Discovery(Broadcast.DEFAULT_PORT)
  discovery.thread.join()
