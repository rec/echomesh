from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import yaml

from six.moves import queue

from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util import Log

LOGGER = Log.logger(__name__)

# See http://docs.python.org/2/howto/sockets.html

MAX_SIZE = 1024

SEGMENT = '\n---\n'
TIMEOUT = 0.1

class Socket(MasterRunnable):
  def __init__(self, port, bind_port, hostname, socket_type):
    super(Socket, self).__init__()
    self.port = port
    self.bind_port = bind_port
    self.hostname = hostname
    self.socket_type = socket_type
    self.socket = None
    self.buffer = ''
    self.queue = queue.Queue()
    self.max_size = MAX_SIZE

  def receive(self):
    if not self.is_running:
      return False

    res = self.socket.recv(self.max_size)
    if not res:
      # An empty packet means it's all over.
      # http://docs.python.org/2/howto/sockets.html
      self.pause()
      return False

    self.buffer += res
    parts = self.buffer.split(SEGMENT)
    self.buffer = parts.pop()
    for part in parts:
      if part:
        try:
          yaml_part = yaml.safe_load(part)
        except:
          LOGGER.error("Didn't understand incoming part %s", part, exc_info=1)
        else:
          self.queue.put(yaml_part)
    return True

  def send(self, timeout=TIMEOUT):
    if self.is_running:
      try:
        item = self.queue.get(timeout=timeout)
      except queue.Empty:
        return

      data = yaml.safe_dump(item) + SEGMENT
      while data:
        packet, data = data[0:self.max_size], data[self.max_size:]
        self._raw_send(packet)

  def _raw_send(self, packet):
    pass

  def _on_run(self):
    super(Socket, self)._on_run()

    self.socket = socket.socket(socket.AF_INET, self.socket_type)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.max_size)
    try:
      self._start_socket()
    except Exception as e:
      if 'Address already in use' in str(e):
        raise Exception('There is already an echomesh node running on port %d' %
                        self.bind_port)
      self.pause()

  def _start_socket(self):
    self.socket.bind((self.hostname, self.bind_port))

  def _on_pause(self):
    super(Socket, self)._on_pause()
    try:
      self.socket.close()
    except:
      pass
    self.socket = None
