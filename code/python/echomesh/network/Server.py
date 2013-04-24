from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import time
import SocketServer

from six.moves import queue

from echomesh.network import ServerMaker
from echomesh.util import Log
from echomesh.util.thread.ThreadRunnable import ThreadRunnable
from echomesh.util.thread import Lock

QUEUED_WRITES = False

LOGGER = Log.logger(__name__)

class Server(ThreadRunnable):
  def __init__(self, host, port, timeout, max_queue_size=20,
               logging=False, allow_reuse_address=True):
    super(Server, self).__init__()
    self.timeout = timeout
    self.queue = None
    self.bytes_written = 0
    self.next_target = 0
    self.packets = 0
    self.lock = Lock.Lock()
    self.writer = None
    self.server = ServerMaker.make_server(
      self.handle, host, port, timeout, logging, allow_reuse_address)

  def target(self):
    self.server.serve_forever(poll_interval=self.timeout)

  def handle(self, handler):
    self.writer = handler.wfile
    self._on_new_handler()
    with self.lock:
      if self.queue:
        data = []
        while not self.queue.empty():
          data.append(self.queue.get(False))
        self.writer.write(''.join(data))
        self.queue = None

    while self.is_running and self.writer:
      time.sleep(self.timeout)

  def write(self, data):
    with self.lock:
      if self.writer:
        try:
          self.writer.write(data)
          return
        except:
          self.writer = None
          self.lost_connection = True

      if not self.queue:
        self.queue = queue.Queue()
      self.queue.put(data)

  def flush(self):
    self.writer and self.writer.flush()

  def _after_thread_pause(self):
    self.server.shutdown()
    self.server = None

  def _on_new_handler(self):
    pass
