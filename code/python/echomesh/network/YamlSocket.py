from __future__ import absolute_import, division, print_function, unicode_literals

from six.moves import queue

import socket
import time
import yaml

from echomesh.base import Yaml
from echomesh.network import BroadcastSocket
from echomesh.network.QueueReader import QueueReader
from echomesh.network.SocketThread import SocketThread
from echomesh.network.SelectLoop import SelectLoop
from echomesh.util.thread.MasterRunnable import MasterRunnable

TIMEOUT = 0.5

class YamlSocket(MasterRunnable):
  def __init__(self, timeout, callback, send_socket, receive_socket):
    super(YamlSocket, self).__init__()
    self.timeout = timeout
    self.callback = callback
    self.buffer = ''

    def send_iterator():
      while self.is_running:
        try:
          y = self._send.queue.get(self.timeout)
          print('22222', y)
          yield y
          yield {}  # Add padding for Yaml's off-by-one issue.
        except queue.Empty:
          continue

    def send_loop():
      yaml.safe_dump_all(send_iterator(), self._send.socket)

    def receive_loop():
      reader = QueueReader(self._receive.queue, self, self.timeout)
      for y in yaml.safe_load_all(reader):
        print('1111111111')
        if not self.is_running:
          return
        if y:  # Remove padding from Yaml's "off by one" issue.
          print('1111111111', y)
          self.callback(y)

    self._send = SocketThread(send_socket, target=send_loop, name='send_thread')
    self._receive = SocketThread(receive_socket, target=receive_loop,
                                 name='receive_thread')

    self.add_mutual_stop_slave(self._send, self._receive)

  def send(self, data):
    self._send.queue.put(data)


class DataSocket(YamlSocket):
  def __init__(self, port, timeout, callback):
    try:
      send_socket = BroadcastSocket.Send(port)
      receive_socket = BroadcastSocket.Receive(port)
    except socket.error as e:
      if e.errno == errno.EADDRINUSE:
        raise Exception('A DataSocket is already running on port %d'  % port)
      else:
        raise
    super(DataSocket, self).__init__(
      timeout, callback, send_socket, receive_socket)
    self.select_loop = SelectLoop(self._receive)
    self.add_slave(self.select_loop)

