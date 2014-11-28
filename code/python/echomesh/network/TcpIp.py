from __future__ import absolute_import, division, print_function, unicode_literals

import socket

from echomesh.network import Socket

MAX_SERVER_CONNECTIONS = 8

class TcpIp(Socket.Socket):
    def __init__(self, port, bind_port, hostname):
        super(TcpIp, self).__init__(
            port, bind_port, hostname, socket.SOCK_STREAM)

class Client(TcpIp):
    def _start_socket(self):
        self.socket.connect((self.hostname, self.port))

class Server(TcpIp):
    def __init__(self, port, bind_port=None, hostname=None,
                 max_connections=MAX_SERVER_CONNECTIONS):
        super(Server, self).__init__(port, bind_port or port,
                                     hostname or socket.gethostname())
        self.max_connections = max_connections

    def _on_run(self):
        super(Server, self)._on_run()
        self.socket.listen(self.max_connections)
