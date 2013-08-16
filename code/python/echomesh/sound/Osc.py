from __future__ import absolute_import, division, print_function, unicode_literals

import OSC

from echomesh.base import Config
from echomesh.expression import Expression
from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util.thread.ThreadRunnable import ThreadRunnable

LOGGER = Log.logger(__name__)

class OscClient(ThreadRunnable):
  def __init__(self):
    Config.add_client(self)

  def config_update(self, get):
    port = get('osc', 'client', 'port')
    host = get('osc', 'client', 'host')
    if self.port != port or self.host != host:
      self.client = None

  def target(self):
    if not self.client:
      pass

  def _on_run(self):
    super(OscClient, self)._on_run()
    self.client = None
    self.port = None
    self.host = None
    Config.add_client(self)

  def _on_pause(self):
    Config.remove_client(self)
    super(OscClient, self)._on_pause()
    self.client.close()
    self.client = None


class OscServer(ThreadRunnable):
  def __init__(self):
    super(OscServer, self).__init__()
    self.server = None
    self.port = None
    Config.add_client(self)

  def config_update(self, get):
    port = get('osc', 'server', 'port')
    if port == self.port:
      return
    if self.server:
      self.server.close()
      self.server = None
    self.port = port
    self.server = OSC.OSCServer(('', port), None, port)
    self.server.socket.settimeout(Expression.convert(get('network', 'timeout')))

  def target(self):
    while self.is_running:
      self.server.serve_forever()

  def _on_pause(self):
    super(OscServer, self)._on_pause()
    self.server.close()

  def handler(self, addr, tags, data, client_address):
    print('OscServer.handler', addr, tags, data, client_address)

class Osc(MasterRunnable):
  def __init__(self, use_client, use_server):
    super(Osc, self).__init__()
    self.client = use_client and OscClient()
    self.server = use_server and OscServer()
    self.add_slave(self.client, self.server)
