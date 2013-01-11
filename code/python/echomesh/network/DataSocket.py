import Queue
import socket

import threading
import time
import yaml

from echomesh.config import Config
from echomesh.network import BroadcastSocket
from echomesh.util import Log
from echomesh.util.thread import ThreadLoop
from echomesh.util.thread import Closer

LOGGER = Log.logger(__name__)

class _Receive(ThreadLoop.ThreadLoop):
  def __init__(self, port, timeout, callback):
    super(Receive, self).__init__()
    self.socket = BroadcastSocket.Receive(port)
    self.timeout = timeout
    self.callback = callback

  def run(self):
    pckt = self.socket.receive(self.timeout)
    if pckt:
      LOGGER.info('receiving %s', pckt)
      self.callback(yaml.safe_load(pckt))


class _Send(ThreadLoop.ThreadLoop):
  def __init__(self, port, timeout):
    super(Send, self).__init__()
    self.socket = BroadcastSocket.Send(port)
    self.timeout = timeout
    self.queue = Queue.Queue()

  def run(self):
    try:
      item = self.queue.get(True, self.timeout)
      value = yaml.safe_dump(item)
      self.socket.write(value)
    except Queue.Empty:
      pass
    if self.is_open:
      time.sleep(self.timeout)


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
    self.add_openable_mutual(self.receive_socket, self.send_socket,
                             threading.Thread(target=self._run_receive),
                             threading.Thread(target=self._run_send))

    self.send = self.queue.put

  def _run_receive(self):
    pckt = self.receive_socket.receive(self.timeout)
    if pckt:
      LOGGER.info('receiving %s', pckt)
      self.callback(yaml.safe_load(pckt))

  def _run_send(self):
    try:
      item = self.queue.get(True, self.timeout)
      value = yaml.safe_dump(item)
      self.send_socket.write(value)
    except Queue.Empty:
      pass
    if self.is_open:
      time.sleep(self.timeout)

