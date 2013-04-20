from __future__ import absolute_import, division, print_function, unicode_literals

import SocketServer

from six.moves import queue

from echomesh.util import Log
from echomesh.util.thread.ThreadLoop import ThreadLoop

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

class Server(ThreadLoop):
  def __init__(self, host, port, timeout, logging=False):
    super(Server, self).__init__()
    self.server = None
    self.host = host
    self.port = port
    self.timeout = timeout
    self.handler = None
    self.queue = queue.Queue()
    self.logging = logging

  def _before_thread_start(self):
    server = self
    class Handler(SocketServer.StreamRequestHandler):
      def handle(self):
        LOGGER.debug('Successfully registered a handler %s', self)
        server.handler = self
        try:
          self.wfile.write('\n')
          self.rfile.read()
        except:
          LOGGER.error('')
          raise
    server_maker = LoggingServer if self.logging else SocketServer.TCPServer
    self.server = server_maker((self.host, self.port), Handler)
    self.server.timeout = self.timeout
    LOGGER.debug('Server created for %s:%d', self.host, self.port)

  def write(self, data):
    self.queue.put(data)

  def reade(self):
    return self.handler.rfile.read()

  def _after_thread_pause(self):
    self.server.shutdown()
    self.server = None

  def single_loop(self):
    self.server.handle_request()
    if self.handler:
      data = []
      while not self.queue.empty():
        data.append(self.queue.get(False))
      data = ''.join(data)
      try:
        self.handler.wfile.write(data)
      except:
        LOGGER.error('Socket hung up on other end.', raw=True)
        self.pause()

