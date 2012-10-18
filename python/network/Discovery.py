from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import threading
import traceback
import yaml
import Queue

from network import Broadcast
from util import Openable
from util import Log

LOGGER = Log.logger(__name__)

class Discovery(Openable.Openable):
  DOCUMENT_START = '---\n'
  DOCUMENT_END = '....\n'

  def __init__(self, config, callbacks=None):
    Openable.Openable.__init__(self)
    self.config = config
    self.queue = Queue.Queue()

    self.callbacks = callbacks

    self.is_running = True

    port = self.config['discovery']['port']
    self.receive_socket = Broadcast.ReceiveSocket(port)
    self.send_socket = Broadcast.SendSocket(port)

    self.receive_thread = threading.Thread(target=self._run_receive)
    self.send_thread = threading.Thread(target=self._run_send)
    LOGGER.info('Starting discovery on port %d', port)

  def start(self):
    self.receive_thread.start()
    self.send_thread.start()

  def close(self):
    Openable.Openable.close(self)
    self.receive_socket.close()
    self.send_socket.close()

  def send(self, data=None):
    self.queue.put(data or self.discovery_data)

  def join(self):
    self.receive_thread.join()
    self.send_thread.join()

  def _run_receive(self):
    try:
      while self.is_open:
        pckt = self.receive_socket.receive(self.config['discovery']['timeout'])
        if pckt:
          data = yaml.safe_load(pckt)
          self.callbacks.get(data['type'], self._error)(data)
    except:
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
    except:
      LOGGER.critical(traceback.format_exc())
      self.close()

  def _error(self, data):
    LOGGER.error('No callbacks for type %s', data['type'])
