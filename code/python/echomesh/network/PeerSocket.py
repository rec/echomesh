from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Name
from echomesh.remote import Command
from echomesh.network import DataSocket
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util.math import Units

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
    Command.execute(self.echomesh, **data)

  def send(self, data):
    if self.is_running:
      data['source'] = Name.NAME
      self.socket.send(data)

  def _on_start(self):
    if not self.socket:
      self._make_socket()

  def _make_socket(self):
    self.socket = DataSocket.DataSocket(self.port, self.timeout, self.router)
    self.add_mutual_stop_slave(self.socket)
    self.socket.start()

  def config_update(self, get):
    self.port, old_port = get('discovery', 'port'), self.port
    self.timeout = int(Units.convert(get('discovery', 'timeout')))
    if self.is_running and self.socket:
      if port == old_port:
        self.socket.timeout = timeout
      else:
        self.port = port
        self.remove_slave(self.socket)
        self.socket.stop()
        self._make_socket()
