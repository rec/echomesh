from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Name
from echomesh.command import Router
from echomesh.network import DataSocket
from echomesh.network import Peers
from echomesh.util.thread.RunnableOwner import RunnableOwner

class PeerSocket(RunnableOwner):
  def __init__(self, echomesh):
    super(PeerSocket, self).__init__()
    self.peers = Peers.Peers(echomesh)
    self.socket = DataSocket.DataSocket(Config.get('discovery', 'port'),
                                        Config.get('discovery', 'timeout'),
                                        Router.router(echomesh, self.peers))

    self.add_slave(self.peers)
    self.add_mutual_stop_slave(self.socket)

  def send(self, data):
    data['source'] = Name.NAME
    self.socket.send(data)
