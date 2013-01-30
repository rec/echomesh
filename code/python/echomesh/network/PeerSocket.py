from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Name
from echomesh.command import Router
from echomesh.network import DataSocket
from echomesh.network import Peers
from echomesh.util.thread.MasterRunnable import MasterRunnable

class PeerSocket(MasterRunnable):
  def __init__(self, echomesh):
    super(PeerSocket, self).__init__()
    self.peers = Peers.Peers(echomesh)
    self.add_slave(self.peers)
    self.port = -1
    self.socket = None
    self.router = Router.router(echomesh, self.peers)

    Config.add_client(self)

  def send(self, data):
    if self.is_running:
      data['source'] = Name.NAME
      self.socket.send(data)

  def start(self):
    if not self.socket:
      self._make_socket()
    super(PeerSocket, self).start()

  def _make_socket(self):
    self.socket = DataSocket.DataSocket(self.port, self.timeout, self.router)
    self.add_mutual_stop_slave(self.socket)
    self.socket.start()

  def config_update(self, get):
    self.port, old_port = get('discovery', 'port'), self.port
    self.timeout = get('discovery', 'timeout')
    if self.is_running and self.socket:
      if port == old_port:
        self.socket.timeout = timeout
      else:
        self.port = port
        self.remove_slave(self.socket)
        self.socket.stop()
        self._make_socket()
