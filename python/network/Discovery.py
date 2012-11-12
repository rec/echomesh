from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import errno
import socket
import threading
import traceback
import yaml
import Queue

from config import Config
from network import Address
from network import Broadcast
from util.Closer import Closer
from util.ThreadLoop import ThreadLoop
from util import Log

DEFAULT_TIMEOUT = 0.500
DEFAULT_PORT = 1238
LOGGER = Log.logger(__name__)

def _timeout():
  return Config.get(('discovery', 'timeout'), DEFAULT_TIMEOUT)

class ReceiveThread(ThreadLoop):
  def __init__(self, port, callback):
    super(ReceiveThread, self).__init__()
    self.socket = Broadcast.ReceiveSocket(port)
    self.callback = callback

  def run(self):
    pckt = self.socket.receive(_timeout())
    if pckt:
      self.callback(yaml.safe_load(pckt))

class SendThread(ThreadLoop):
  def __init__(self, port, queue):
    super(SendThread, self).__init__()
    self.socket = Broadcast.SendSocket(port)
    self.queue = queue

  def run(self):
    try:
      item = self.queue.get(True, _timeout())
      value = yaml.safe_dump(item)
      self.socket.write(value)
    except Queue.Empty:
      pass

class Discovery(Closer):
  DOCUMENT_START = '---\n'
  DOCUMENT_END = '....\n'

  def __init__(self, callbacks):
    super(Discovery, self).__init__()
    self.callbacks = callbacks
    self.queue = Queue.Queue()

  def start(self):
    port = Config.get(['discovery', 'port'], DEFAULT_PORT)
    try:
      self.receive_thread = ReceiveThread(port, self.callbacks)
      self.mutual_closer(self.receive_thread)

      self.send_thread = SendThread(port, self.queue)
      self.mutual_closer(self.send_thread)

    except socket.error as e:
      if e.errno == errno.EADDRINUSE:
        LOGGER.error('An echomesh node is already running on this machine')
        self.close()
        return False
      else:
        raise

    self.receive_thread.start()
    self.send_thread.start()
    LOGGER.info('Started discovery on port %d', port)
    return True

  def send(self, **data):
    if 'source' not in data:
      data = dict(**data)
      data['source'] = Address.NODENAME
    self.queue.put(data)

  def join(self):
    try:
      self.receive_thread.join()
    except:
      pass

    try:
      self.send_thread.join()
    except:
      pass


  def _error(self, data):
    LOGGER.error('No callbacks for type %s', data['type'])
