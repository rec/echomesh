from __future__ import absolute_import, division, print_function, unicode_literals

import select
import socket

from echomesh.util.thread.MasterRunnable import MasterRunnable

# See http://docs.python.org/2/howto/sockets.html

class Socket(MasterRunnable):
  def __init__(self, port, bind_port, hostname, socket_type):
    super(Socket, self).__init__()
    self.port = port
    self.bind_port = bind_port
    self.hostname = hostname
    self.socket_type = socket_type
    self.socket = None

  def _on_start(self):
    self.socket = socket.socket(socket.AF_INET, self.socket_type)
    self._start_socket()

  def _start_socket(self):
    self.socket.bind((self.hostname, self.bind_port))

  def _on_stop(self):
    self.socket.close()
    self.socket = None

