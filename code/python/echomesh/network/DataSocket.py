import Queue
import time
import yaml

from echomesh.config import Config
from echomesh.network import BroadcastSocket
from echomesh.util import Log
from echomesh.util import ThreadLoop

LOGGER = Log.logger(__name__)

def _timeout():
  return Config.get('discovery', 'timeout')

class Receive(ThreadLoop.ThreadLoop):
  def __init__(self, port, callback):
    super(Receive, self).__init__()
    self.socket = BroadcastSocket.Receive(port)
    self.callback = callback

  def run(self):
    pckt = self.socket.receive(_timeout())
    if pckt:
      LOGGER.info('receiving %s', pckt)
      self.callback(yaml.safe_load(pckt))


class Send(ThreadLoop.ThreadLoop):
  def __init__(self, port):
    super(Send, self).__init__()
    self.socket = BroadcastSocket.Send(port)
    self.queue = Queue.Queue()

  def run(self):
    try:
      item = self.queue.get(True, _timeout())
      value = yaml.safe_dump(item)
      self.socket.write(value)
    except Queue.Empty:
      pass
    if self.is_open:
      time.sleep(_timeout())

  def send(self, item):
    self.queue.put(item)
