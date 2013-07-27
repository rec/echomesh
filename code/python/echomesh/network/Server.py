from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import time
import SocketServer

from six.moves import queue

from echomesh.base import Yaml
from echomesh.network import ServerMaker
from echomesh.util import Log
from echomesh.util.string.LineReader import LineReader
from echomesh.util.thread.ThreadRunnable import ThreadRunnable
from echomesh.util.thread import Lock

LOGGER = Log.logger(__name__)

LOG_ALL_DATA = not True

MAX_QUEUE_SIZE = 16

FILE = None

def _write(text, flush=False):
  global FILE
  if not FILE:
    FILE = open('/tmp/echomesh.socket.out.txt', 'w')
  FILE.write(text)
  if flush:
    FILE.flush()

class Server(ThreadRunnable):
  def __init__(self, host, port, timeout, read_callback=None, max_queue_size=20,
               logging=False, allow_reuse_address=True, debug=False):
    LOGGER.debug('Creating Server')
    super(Server, self).__init__()
    self.timeout = timeout
    self.queue = None
    self.config = []
    self.debug = debug
    self.bytes_written = 0
    self.next_target = 0
    self.packets = 0
    self.lock = Lock.Lock()
    self.handler = None
    LOGGER.debug('About to open IP server %s:%s', host, port)
    self.server = ServerMaker.make_server(
      self._handle, host, port, timeout, logging, allow_reuse_address)
    LOGGER.debug('Ip server opened')
    self.line_reader = LineReader(read_callback)

  def target(self):
    self.server.serve_forever(poll_interval=self.timeout)

  def _write(self, data):
    if self.handler and data:
      d = Yaml.encode_one(data)
      self.handler.wfile.write(d)
      self.handler.wfile.write(Yaml.SEPARATOR)
      if self.debug or LOG_ALL_DATA:
        _write(d)
        _write(Yaml.SEPARATOR, True)
      self.handler.wfile.flush()
    else:
      if not self.queue:
        self.queue = queue.Queue(MAX_QUEUE_SIZE)
      self.queue.put(data)

  def _handle(self, handler):
    LOGGER.debug('IP connection has started up.')
    with self.lock:
      self.handler = handler
      for c in self.config:
        self._write(c)
    while True:
      try:
        self._write(self.queue.get(False))
      except queue.Empty:
        break
    LOGGER.debug('configuration has been sent.')

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
        self.line_reader.add(data)

      if disconnect:
        time.sleep(self.timeout)

  def set_config(self, *config):
    with self.lock:
      self.config = config
      if self.handler:
        for c in config:
          self._write(c)

  def write(self, **data):
    with self.lock:
      self._write(data)

  def _after_thread_pause(self):
    self.server.shutdown()
    self.server = None
