from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log

LOGGER = Log.logger(__name__)

Description = collections.namedtuple(
  'SocketDescription',
  ['bind_port', 'create', 'hostname', 'port', 'socket_type', 'send', 'start'])

class Broadcast(Description):
  def __init__(**kwds):
    super(Broadcast, self).__init__(
      hostname='', socket_type=socket.SOCK_DGRAM, **kwds)

class BroadcastSend(Broadcast):
  def __init__(**kwds):
    def create():

    def send(socket, data):
      socket.sendto(data, ('<broadcast>', self.port))

    def start():


    super(BroadcastSend, self).__init__(
      create=create, send=send, start=start, **kwds)

