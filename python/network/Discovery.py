from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import threading
import traceback
import yaml
import Queue

from network import Broadcast

class Discovery(object):
  def __init__(self, port, timeout, callbacks=None):
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
    self.send_socket.close()
    self.receive_socket.close()

  def send(self, data=None):
    self.queue.put(data or self.discovery_data)

  def join(self):
    self.receive_thread.join()
    self.send_thread.join()

  def _run_receive(self):
    try:
      for data in yaml.safe_load_all(self.receive_socket):
        self.callbacks.get(data['type'], self._error)(data)
    except:
      traceback.print_stack()
      self.close()

  def _run_send(self):
    try:
      def generator():
        while self.send_socket.is_open:
          try:
            value = self.queue.get(True, self.timeout)
            yield value
          except Queue.Empty:
            pass
      yaml.safe_dump_all(generator(), self.send_socket)
    except:
      traceback.print_stack()

  def _error(self, data):
    print('No callbacks for type', data['type'])
