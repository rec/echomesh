from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import errno
import socket
import threading
import traceback
import yaml
import Queue

from network import Address
from network import Broadcast
from util.Closer import Closer
from util import Log

LOGGER = Log.logger(__name__)

class Discovery(Closer):
  DOCUMENT_START = '---\n'
  DOCUMENT_END = '....\n'

  def __init__(self, config, callbacks):
    Closer.__init__(self)
    self.config = config
    self.queue = Queue.Queue()

    self.callbacks = callbacks

  def start(self):
    port = self.config['discovery']['port']
    try:
      self.receive_socket = Broadcast.ReceiveSocket(port)
      self.add_closer(self.receive_socket)
      self.send_socket = Broadcast.SendSocket(port)
      self.add_closer(self.send_socket)

    except socket.error as e:
      if e.errno == errno.EADDRINUSE:
        LOGGER.error('An echomesh node is already running on this machine')
        self.close()
        return False
      else:
        raise

    self.receive_thread = threading.Thread(target=self._run_receive)
    self.send_thread = threading.Thread(target=self._run_send)
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

  def _run_receive(self):
    try:
      while self.is_open:
        pckt = self.receive_socket.receive(self.config['discovery']['timeout'])
        if pckt:
          self.callbacks(yaml.safe_load(pckt))
      LOGGER.debug('receive thread ending')
    except:
      if self.is_open:
        LOGGER.critical(traceback.format_exc())
        self.close()

  def _run_send(self):
    try:
      while self.is_open:
        try:
          item = self.queue.get(True, self.config['discovery']['timeout'])
          value = yaml.safe_dump(item)
          self.send_socket.write(value)
        except Queue.Empty:
          pass
      LOGGER.debug('send thread ending')
    except:
      if self.is_open:
        LOGGER.critical(traceback.format_exc())
        self.close()

  def _error(self, data):
    LOGGER.error('No callbacks for type %s', data['type'])
