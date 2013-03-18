from __future__ import absolute_import, division, print_function, unicode_literals

import errno
import socket

from six.moves import queue

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

    try:
      self.receive_socket = BroadcastSocket.Receive(port)
      self.send_socket = BroadcastSocket.Send(port)
    except socket.error as e:
      if e.errno == errno.EADDRINUSE:
        raise Exception('A DataSocket is already running on port %d'  % port)
      else:
        raise

  def _on_run(self):
    self.receive_socket.run()
    self.send_socket.run()
    self.select_loop = SelectLoop.SelectLoop(self.receive_socket)
    self.select_loop.run()
    self.send_thread = ThreadLoop.ThreadLoop(single_loop=self.send_socket.send)
    self.send_thread.run()

    def receive():
      try:
        item = self.receive_socket.queue.get(timeout=self.timeout)
      except queue.Empty:
        return
      self.callback(item)

    self.receive_thread = ThreadLoop.ThreadLoop(single_loop=receive)
    self.receive_thread.run()
    self.send = self.send_socket.queue.put

    self.add_slave(self.select_loop, self.send_thread, self.receive_thread,
                   self.receive_socket, self.send_socket)


