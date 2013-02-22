from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import time

from six.moves import queue

from echomesh.base import Yaml
from echomesh.network import BroadcastSocket
from echomesh.network import SelectLoop
from echomesh.util import Log
from echomesh.util.thread import ThreadLoop
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

class DataSocket(MasterRunnable):
  def __init__(self, port, timeout, callback):
    super(DataSocket, self).__init__()
    self.timeout = timeout
    self.callback = callback
    self.queue = queue.Queue()

    try:
      self.receive_socket = BroadcastSocket.Receive(port)
      self.send_socket = BroadcastSocket.Send(port)
    except socket.error as e:
      if e.errno == errno.EADDRINUSE:
        raise Exception('A DataSocket is already running on port %d'  % port)
      else:
        raise
    self.send = self.queue.put

  def _on_start(self):
    self.receive_socket.start()
    self.send_socket.start()
    self.select_loop = SelectLoop.SelectLoop(self.receive_socket)
    self.select_loop.start()
    self.send_thread = ThreadLoop.ThreadLoop(single_loop=self.send_socket.send)
    self.send_thread.start()

    self.add_slave(self.select_loop, self.send_thread,
                   self.receive_socket, self.send_socket)


