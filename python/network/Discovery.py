from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import os
import threading
import time
import yaml
import Queue

from network import Address
from network import Broadcast
from network import Locker

DEFAULT_TIMEOUT = 0.2
DISCOVERY_TYPE = 'discovery'

# TODO: extract this function entirely...
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
    self.queue = Queue.Queue()

    self.callbacks = copy.deepcopy(callbacks)
    assert DISCOVERY_TYPE not in self.callbacks
    self.callbacks[DISCOVERY_TYPE] = self._receive_discovery

    self.lock = threading.RLock()
    self.discovery_data = _get_discovery_data()
    self.is_running = True
    self.receive_socket = Broadcast.SocketReader(self.port, timeout=timeout)
    self.send_socket = Broadcast.SendSocket(self.port)

    self.send(self.discovery_data)

    self.receive_thread = threading.Thread(target=self._run_receive)
    self.send_thread = threading.Thread(target=self._run_send)
    self.receive_thread.start()
    self.send_thread.start()

  def close(self):
    self.send_socket.close()
    self.receive_socket.close()

  def send(self, data=None):
    self.queue.put(data or self.discovery_data)

  def _run_receive(self):
    for data in yaml.safe_load_all(self.receive_socket):
      self.callbacks.get(data['type'], self._error)(data)

  def _run_send(self):
    def generator():
      while self.send_socket.is_open:
        try:
          value = self.queue.get(True, self.timeout)
          yield value
        except Queue.Empty:
          pass
    yaml.safe_dump_all(generator(), self.send_socket)

  def _error(self, data):
    print('No callbacks for type', data['type'])

  def _receive_discovery(self, data):
    with Locker.Locker(self.lock):
      nodename = data['nodename']
      c = self.clients.get(nodename, None)
      if c == data:
        return
      print('New client', data)
      self.clients[nodename] = data
    self.send(self.discovery_data)

