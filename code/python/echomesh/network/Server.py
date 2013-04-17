from __future__ import absolute_import, division, print_function, unicode_literals

import SocketServer

from compatibility.weakref import WeakSet

from echomesh.util import Log
from echomesh.util.thread.ThreadRunnable import ThreadRunnable

LOGGER = Log.logger(__name__)

class Server(ThreadRunnable):
  def __init__(self, host, port, timeout):
    super(Server, self).__init__()
    self.server = None
    self.host = host
    self.port = port
    self.timeout = timeout
    self.handlers = set()

  def _before_thread_start(self):
    def Handler(*args, **kwds):
      s = SocketServer.StreamRequestHandler(*args, **kwds)
      self.handlers.add(s)
      return s

    self.server = SocketServer.TCPServer((self.host, self.port), Handler)
    LOGGER.info('Server created for %s:%d', self.host, self.port)

  def send(self, data):
    for h in self.handlers:
      h.wfile.write(data)

  def _after_thread_pause(self):
    self.server.shutdown()
    self.server = None

  def target(self):
    LOGGER.info('Starting to serve on %s:%d', self.host, self.port)
    self.server.serve_forever(self.timeout)
