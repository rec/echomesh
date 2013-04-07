from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Name
from echomesh.expression import Units
from echomesh.network import DataSocket
from echomesh.remote import Remote
from echomesh.util.thread.MasterRunnable import MasterRunnable

USE_YAML_SOCKET = True

class PeerSocket(MasterRunnable):
  def __init__(self, instance, peers):
    super(PeerSocket, self).__init__()
    self.instance = instance
    self.peers = peers
    self.add_slave(self.peers)
    self.port = -1
    self.socket = None

    Config.add_client(self.config_update)

  def router(self, data):
    Remote.execute(self.instance, **data)

  def send(self, data):
    if self.is_running:
      data['source'] = Name.NAME
      self.socket.send(data)

  def _on_run(self):
    super(PeerSocket, self)._on_run()
    if not self.socket:
      self._make_socket()

  def _make_socket(self):
    self.socket = DataSocket.DataSocket(self.port, self.timeout, self.router)
    self.add_mutual_pause_slave(self.socket)
    self.socket.run()

  def config_update(self, get):
    self.port, old_port = get('discovery', 'port'), self.port
    self.timeout = Units.convert(get('discovery', 'timeout'))
    if self.is_running and self.socket:
      if self.port == old_port:
        self.socket.timeout = self.timeout
      else:
        self.remove_slave(self.socket)
        self.socket.pause()
        self._make_socket()
