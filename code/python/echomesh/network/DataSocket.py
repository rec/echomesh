from __future__ import absolute_import, division, print_function, unicode_literals

import errno
import socket

from six.moves import queue

from echomesh.network import BroadcastSocket
from echomesh.network import SelectLoop
from echomesh.base import Quit
from echomesh.util.thread import ThreadLoop
from echomesh.util.thread.MasterRunnable import MasterRunnable

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
    self.send_thread = ThreadLoop.ThreadLoop(single_loop=self.send_socket.send,
                                             name='DataSocket.send')
    self.send_thread.run()

    def receive():
      try:
        if not Quit.QUITTING:
          item = self.receive_socket.queue.get(timeout=self.timeout)
      except queue.Empty:
        return
      except:
        if not Quit.QUITTING:
          raise

      try:
        if not Quit.QUITTING:
          self.callback(item)
      except Exception as e:
        print('DataSocket.receive:', e)

    self.receive_thread = ThreadLoop.ThreadLoop(single_loop=receive,
                                                name='DataSocket.receive')
    self.receive_thread.run()
    self.send = self.send_socket.queue.put

    self.add_slave(self.select_loop, self.send_thread, self.receive_thread,
                   self.receive_socket, self.send_socket)


