from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import threading
import traceback
import yaml
import Queue

from network import Broadcast
from util.Openable import Openable

class Discovery(Openable):
  DOCUMENT_START = '---\n'
  DOCUMENT_END = '....\n'

  def __init__(self, port, timeout, callbacks=None):
    Openable.__init__(self)
    self.port = port
    self.timeout = timeout
    self.queue = Queue.Queue()

    self.callbacks = callbacks

    self.is_running = True
    self.receive_socket = Broadcast.SocketReader(self.port, timeout=timeout)
    self.send_socket = Broadcast.SendSocket(self.port)

    self.receive_thread = threading.Thread(target=self._run_receive)
    self.send_thread = threading.Thread(target=self._run_send)

  def start(self):
    self.receive_thread.start()
    self.send_thread.start()

  def close(self):
    Openable.close(self)
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
        packet = self.receive_socket.receive()
        if packet:
          data = yaml.safe_load(packet)
          self.callbacks.get(data['type'], self._error)(data)
    except:
      print(traceback.format_exc())
      self.close()

  def _run_send(self):
    try:
      while self.is_open:
        try:
          item = self.queue.get(True, self.timeout)
          value = yaml.safe_dump(item)
          self.send_socket.write(value)
        except Queue.Empty:
          pass
    except:
      print(traceback.format_exc())
      self.close()

  def _error(self, data):
    print('No callbacks for type', data['type'])
