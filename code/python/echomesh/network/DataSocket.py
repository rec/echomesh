import Queue
import socket
import time
import yaml

from echomesh.base import Config
from echomesh.network import BroadcastSocket
from echomesh.util import Log
from echomesh.util.thread import Closer
from echomesh.util.thread import ThreadLoop

LOGGER = Log.logger(__name__)

class DataSocket(Closer.Closer):
  def __init__(self, port, timeout, callback):
    super(DataSocket, self).__init__()
    self.timeout = timeout
    self.callback = callback
    self.queue = Queue.Queue()

    try:
      self.receive_socket = BroadcastSocket.Receive(port)
      self.send_socket = BroadcastSocket.Send(port)
    except socket.error as e:
      if e.errno == errno.EADDRINUSE:
        raise Exception('A DataSocket is already running on port %d'  % port)
      else:
        raise

    send = ThreadLoop.ThreadLoop(target=self._send, name='send')
    receive = ThreadLoop.ThreadLoop(target=self._receive, name='receive')

    self.add_slave_closer(self.receive_socket, self.send_socket, receive, send)
    self.send = self.queue.put

  def _receive(self):
    pckt = self.receive_socket.receive(self.timeout)
    if pckt:
      LOGGER.info('receiving %s', pckt)
      self.callback(yaml.safe_load(pckt))

  def _send(self):
    try:
      item = self.queue.get(True, self.timeout)
      value = yaml.safe_dump(item)
      self.send_socket.write(value)
    except Queue.Empty:
      pass
    if self.is_running:
      time.sleep(self.timeout)

