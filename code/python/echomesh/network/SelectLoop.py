from __future__ import absolute_import, division, print_function, unicode_literals

import select

from echomesh.network.SocketThread import SocketThread
from echomesh.util import Log
from echomesh.util.thread import ThreadLoop

LOGGER = Log.logger(__name__)

BUFFER_SIZE = 1024
TIMEOUT = 0.100

class SelectLoop(ThreadLoop.ThreadLoop):
  def __init__(self, *sockets):
    super(SelectLoop, self).__init__()
    self.sockets = dict((s.socket, s) for s in sockets)

  def single_loop(self):
    try:
      result = select.select(self.sockets.keys(), [], [], TIMEOUT)
    except Exception as e:
      self._remove_bad()
    else:
      for socket in result[0]:
        s = self.sockets.get(socket)
        if not s:
          LOGGER.error("Got an update for a socket we didn't recognize.")
        elif not s.receive():
          self.remove_socket(socket)
        else:
          LOGGER.print("got something!")

  def remove_socket(self, socket):
    s = self.sockets.get(socket)
    if s:
      del self.sockets[socket]
      s.stop()
    else:
      LOGGER.error("Tried to remove a socket we didn't know about.")

  def _remove_bad(self):
    for socket in self.sockets:
      try:
        select.select([socket], [], [], timeout=0)
      except:
        bad.append(socket)

    if bad:
      for socket in bad:
        LOGGER.error('A socket %s went bad.', str(st))
        self._remove_socket(socket)
    else:
      LOGGER.error('Tried to remove_bad, but found none.')
