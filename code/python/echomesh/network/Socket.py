from __future__ import absolute_import, division, print_function, unicode_literals

import select
import socket

from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util import Log

LOGGER = Log.logger(__name__)

# See http://docs.python.org/2/howto/sockets.html

BUFFER_SIZE = 4096

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
    try:
      self._start_socket()
    except Exception as e:
      if 'Address already in use' in str(e):
        raise Exception('There is already an echomesh node running on port %d' %
                        self.bind_port)

  def _start_socket(self):
    self.socket.bind((self.hostname, self.bind_port))

  def _on_stop(self):
    self.socket.close()
    self.socket = None

  def recv(self):
    return self.is_running and self.socket.recv(BUFFER_SIZE)
