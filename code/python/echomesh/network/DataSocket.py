import Queue
import socket
import time
import yaml

from echomesh.config import Config
from echomesh.network import BroadcastSocket
from echomesh.util import Log
from echomesh.util.thread import ThreadLoop
from echomesh.util.thread import Closer

LOGGER = Log.logger(__name__)

class Receive(ThreadLoop.ThreadLoop):
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


class Send(ThreadLoop.ThreadLoop):
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

  def send(self, item):
    self.queue.put(item)


class SendReceive(Closer.Closer):
  def __init__(self, port, timeout, callback):
    super(SendReceive, self).__init__()
    self._receive = Receive(port, timeout, callback)
    self._send = Send(port, timeout)
    self.mutual_closer(self._receive, self._send)
    self.join = self.join_all
    self.send = self._send.send

  def start(self):
    self._receive.start()
    self._send.start()

def data_socket(port, timeout, callback):
  try:
    return SendReceive(port, timeout, callback)
  except socket.error as e:
    if e.errno == errno.EADDRINUSE:
      LOGGER.error('Another DataSocket is already running on port %d', port)
    else:
      raise
