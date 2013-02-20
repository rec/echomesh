from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import time

from echomesh.base import Yaml
from echomesh.network.SocketThread import SocketThread
from echomesh.util.thread.MasterRunnable import MasterRunnable

class YamlSocket(MasterRunnable):
  def __init__(self, timeout, callback, send_socket, receive_socket):
    super(YamlSocket, self).__init__()
    self.timeout = timeout
    self.callback = callback

    def send_iterator():
      for data in self._send.iterator(timeout):
        yield data
        yield {}  # Add padding for Yaml's off-by-one issue.

    def send_loop():
      yaml.safe_dump_all(send_iterator(), self._send.socket)
    self._send = SocketThread(send_socket, target=send_loop)

    def receive_loop():
      for y in yaml.safe_load_all(self._receive.iterator(self.timeout)):
        if y:  # Remove padding from Yaml's "off by one" issue.
          self.callback(y)
    self._receive = SocketThread(receive_socket, target=receive_loop)

    self.add_mutual_stop_slave(self._send, self._receive)

  def send(self, data)
    self._send.queue.put(data)
