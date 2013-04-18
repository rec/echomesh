from __future__ import absolute_import, division, print_function, unicode_literals

import SocketServer

from six.moves import queue

from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop

LOGGER = Log.logger(__name__)

class TCPServer(SocketServer.TCPServer):
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

class Server(ThreadLoop):
  def __init__(self, host, port, timeout):
    super(Server, self).__init__()
    self.server = None
    self.host = host
    self.port = port
    self.timeout = timeout
    self.handlers = set()
    self.queue = queue.Queue()

  def _before_thread_start(self):
    server = self
    class Handler(SocketServer.StreamRequestHandler):
      def handle(self):
        server.register(self)
        try:
          self.wfile.write('\n')
          self.rfile.read()
        except:
          LOGGER.error('')
          raise
    self.server = SocketServer.TCPServer((self.host, self.port), Handler)
    self.server.timeout = self.timeout
    LOGGER.debug('Server created for %s:%d', self.host, self.port)

  def register(self, handler):
    self.handlers.add(handler)
    LOGGER.debug('Successfully registered a handler %s', handler)

  def send(self, data):
    if self.is_running:
      if self.handlers:
        self._send_one(data)
      else:
        LOGGER.debug('!!! queing data')
        self.queue.put(data)

  def _send_one(self, data):
    for h in self.handlers:
      h.wfile.write(data)

  def _after_thread_pause(self):
    self.server.shutdown()
    self.server = None

  def single_loop(self):
    self.server.handle_request()
    if not self.queue.empty() and self.handlers:
      while not self.queue.empty():
        try:
          data = self.queue.get(False)
        except queue.Empty:
          return
        self._send_one(data)
