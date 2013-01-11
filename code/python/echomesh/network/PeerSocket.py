from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.command import Router
from echomesh.config import Config
from echomesh.network import Address
from echomesh.network import DataSocket
from echomesh.network import Peers
from echomesh.util.thread import Closer

class PeerSocket(Closer.Closer):
  def __init__(self, echomesh):
    super(PeerSocket, self).__init__()
    peers = Peers.Peers(echomesh)
    self.socket = DataSocket.DataSocket(Config.get('discovery', 'port'),
                                        Config.get('discovery', 'timeout'),
                                        Router.router(echomesh, peers))

    self.add_openable_mutual(peers, self.socket)

  def send(self, **data):
    data['source'] = Address.NODENAME
    self.socket.send(data)
