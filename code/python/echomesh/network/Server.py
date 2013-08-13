from __future__ import absolute_import, division, print_function, unicode_literals

import time

from six.moves import queue

from echomesh.base import Yaml
from echomesh.network import ServerMaker
from echomesh.util import Log
from echomesh.util.string.LineReader import LineReader
from echomesh.util.thread.ThreadRunnable import ThreadRunnable
from echomesh.util.thread import Lock

LOGGER = Log.logger(__name__)

LOG_ALL_DATA = not True

FILE = None

def _write(text, flush=False):
  global FILE
  if not FILE:
    FILE = open('/tmp/echomesh.socket.out.txt', 'w')
  FILE.write(text)
  if flush:
    FILE.flush()

class Server(ThreadRunnable):
  def __init__(self, host, port, timeout, read_callback=None, max_queue_size=24,
               logging=False, allow_reuse_address=True, debug=False):
    LOGGER.vdebug('Creating Server')
    super(Server, self).__init__()
    self.timeout = timeout
    self.queue = None
    self.config = []
    self.debug = debug
    self.max_queue_size = max_queue_size
    self.bytes_written = 0
    self.next_target = 0
    self.packets = 0
    self.lock = Lock.Lock()
    self.handler = None
    LOGGER.vdebug('About to open IP server %s:%s', host, port)
    self.server = ServerMaker.make_server(
      self._handle, host, port, timeout, logging, allow_reuse_address)
    LOGGER.vdebug('IP server opened')
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
        self.queue = queue.Queue(self.max_queue_size)
      self.queue.put(data)

  def _handle(self, handler):
    LOGGER.vdebug('IP connection has started up.')
    with self.lock:
      self.handler = handler
      for c in self.config:
        self._write(c)
    while self.queue:
      try:
        self._write(self.queue.get(False))
      except queue.Empty:
        break
    LOGGER.vdebug('configuration has been sent.')

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
