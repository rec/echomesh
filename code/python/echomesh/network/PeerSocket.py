from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Name
from echomesh.network import DataSocket
from echomesh.network import YamlSocket
from echomesh.remote import Remote
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util.math import Units

USE_YAML_SOCKET = True

class PeerSocket(MasterRunnable):
  def __init__(self, echomesh, peers):
    super(PeerSocket, self).__init__()
    self.echomesh = echomesh
    self.peers = peers
    self.add_slave(self.peers)
    self.port = -1
    self.socket = None

    Config.add_client(self)

  def router(self, data):
    Remote.execute(self.echomesh, **data)

  def send(self, data):
    if self.is_running:
      data['source'] = Name.NAME
      self.socket.send(data)

  def _on_start(self):
    if not self.socket:
      self._make_socket()

  def _make_socket(self):
    if Config.get('discovery', 'use_yaml_sockets'):
      self.socket = YamlSocket.DataSocket(self.port, self.timeout, self.router)
    else:
      self.socket = DataSocket.DataSocket(self.port, self.timeout, self.router)
    self.add_mutual_stop_slave(self.socket)
    self.socket.start()

  def config_update(self, get):
    self.port, old_port = get('discovery', 'port'), self.port
    self.timeout = Units.convert(get('discovery', 'timeout'))
    if self.is_running and self.socket:
      if port == old_port:
        self.socket.timeout = timeout
      else:
        self.port = port
        self.remove_slave(self.socket)
        self.socket.stop()
        self._make_socket()
