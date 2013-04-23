from __future__ import absolute_import, division, print_function, unicode_literals

import socket
import time
import SocketServer

from six.moves import queue

from echomesh.util import Log
from echomesh.util.thread.ThreadRunnable import ThreadRunnable
from echomesh.util.thread import Lock

QUEUED_WRITES = False

LOGGER = Log.logger(__name__)

class LoggingServer(SocketServer.TCPServer):
  def close_request(self, request):
    LOGGER.info('Closing request %s', request)
    return SocketServer.TCPServer.close_request(self, request)

  def shutdown_request(self, request):
    LOGGER.info('shutdown request %s', request)
    return SocketServer.TCPServer.shutdown_request(self, request)

  def get_request(self):
    LOGGER.info('get_request')
    return SocketServer.TCPServer.get_request(self)

  def process_request(self, req, address):
    LOGGER.info('process_request %s %s', req, address)
    return SocketServer.TCPServer.process_request(self, req, address)

  def verify_request(self, req, address):
    LOGGER.info('verify_request %s %s', req, address)
    return SocketServer.TCPServer.verify_request(self, req, address)

  def finish_request(self, req, address):
    LOGGER.info('finish_request %s %s', req, address)
    return SocketServer.TCPServer.finish_request(self, req, address)


REPORT_EVERY = 100000

class Server(ThreadRunnable):
  def __init__(self, host, port, timeout, logging=False,
               allow_reuse_address=True):
    super(Server, self).__init__()
    self.timeout = timeout
    self.queue = None
    self.bytes_written = 0
    self.next_target = 0
    self.packets = 0
    self.lock = Lock.Lock()
    self.writer = None

    me = self
    class Handler(SocketServer.StreamRequestHandler):
      def handle(self):
        me.handle(self)

    server_maker = LoggingServer if logging else SocketServer.TCPServer
    self.server = server_maker((host, port), Handler, bind_and_activate=False)
    self.server.allow_reuse_address = allow_reuse_address
    self.server.timeout = self.timeout

  def target(self):
    self.server.server_bind()
    self.server.server_activate()
    self.server.serve_forever(poll_interval=self.timeout)

    LOGGER.debug('Server created for %s:%d', self.host, self.port)

  def handle(self, handler):
    self.writer = handler.wfile
    with self.lock:
      if self.queue:
        data = []
        while not self.queue.empty():
          data.append(self.queue.get(False))
        self.writer.write(''.join(data))
        self.queue = None

    while self.is_running:
      time.sleep(self.timeout)

  def write(self, data):
    with self.lock:
      if not self.writer:
        if not self.queue:
          self.queue = queue.Queue()
        self.queue.put(data)
      else:
        self.writer.write(data)

  def flush(self):
    self.writer and self.writer.flush()

  def _after_thread_pause(self):
    self.server.shutdown()
    self.server = None
