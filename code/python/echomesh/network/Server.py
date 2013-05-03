from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import time
import SocketServer

from six.moves import queue

from echomesh.network import ServerMaker
from echomesh.util import Log
from echomesh.util.thread.ThreadRunnable import ThreadRunnable
from echomesh.util.thread import Lock

LOGGER = Log.logger(__name__)

LOG_ALL_DATA = True

if LOG_ALL_DATA:
  FILE = open('/tmp/echomesh.socket.out.txt', 'w')

class Server(ThreadRunnable):
  def __init__(self, host, port, timeout, read_callback=None, max_queue_size=20,
               logging=False, allow_reuse_address=True):
    super(Server, self).__init__()
    self.timeout = timeout
    self.read_callback = read_callback
    self.queue = None
    self.config = None
    self.bytes_written = 0
    self.next_target = 0
    self.packets = 0
    self.lock = Lock.Lock()
    self.handler = None
    self.server = ServerMaker.make_server(
      self._handle, host, port, timeout, logging, allow_reuse_address)

  def target(self):
    self.server.serve_forever(poll_interval=self.timeout)

  def _write(self, *data):
    if self.handler and data:
      for d in data:
        self.handler.wfile.write(d)
        if LOG_ALL_DATA:
          FILE.write(d)
          FILE.flush()
      self.handler.wfile.flush()

  def _handle(self, handler):
    with self.lock:
      self.handler = handler
      self._write(*self.config)

    while self.is_running:
      with self.lock:
        rfile = self.handler.rfile
        disconnect = not self.handler
      data = None
      if not disconnect:
        try:
          data = rfile.readline()
        except:
          continue
      if data and self.read_callback:
        self.read_callback(data)

      if disconnect:
        time.sleep(self.timeout)

  def set_config(self, *config):
    with self.lock:
      self.config = config
      self._write(*config)

  def write(self, *data):
    with self.lock:
      self._write(*data)

  def _after_thread_pause(self):
    self.server.shutdown()
    self.server = None
