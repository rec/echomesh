from __future__ import absolute_import, division, print_function, unicode_literals

import SocketServer

from echomesh.util import Log

LOGGER = Log.logger(__name__)

LOGGING = True

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


def make_server(callback, host, port, timeout, logging, allow_reuse_address):
  maker = LoggingServer if (logging or LOGGING) else SocketServer.TCPServer
  class Handler(SocketServer.StreamRequestHandler):
    def handle(self):
      callback(self)

  server = maker((host, port), Handler, bind_and_activate=False)
  server.allow_reuse_address = allow_reuse_address
  server.timeout = timeout
  server.server_bind()
  server.server_activate()
  return server

