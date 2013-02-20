from __future__ import absolute_import, division, print_function, unicode_literals

import select

from echomesh.util import Log
from echomesh.util.thread import ThreadLoop

LOGGER = Log.logger(__name__)

class SelectLoop(ThreadLoop.ThreadLoop):
  def __init__(self, *sockets):
    super(SelectLoop, self).__init__()
    # Map Python sockets to our data sockets
    for s in sockets:
      self.add_socket(s)

  def single_loop(self):
    try:
      result = select.select(self.socket_threads.keys(), [], [], timeout=TIMEOUT)
    except:
      self.remove_bad()
    else:
      for socket in result[0]:
        socket_thread = self.socket_threads.get(socket)
        if not socket_thread:
          LOGGER.error("Got an update for a socket we don't know.")
          continue

        packet = socket.recv(BUFFER_SIZE)
        if packet:
          socket_thread.queue.put(packet)
        else:
          LOGGER.debug('A socket %s went dead.', str(socket))
          self.remove_socket(socket)

  def remove_bad(self):
    bad = []
    for socket in self.sockets:
      try:
        select.select([socket], [], [], timeout=0)
      except:
        bad.append(socket)

    if bad:
      for socket in bad:
        LOGGER.debug('A socket %s went bad.', str(socket))
        self.remove_socket(socket)
    else:
      LOGGER.error('Tried to remove_bad, but found none.')

  def add_socket(self, socket_thread):
    self.socket_threads[socket_threads.socket] = socket_threads

  def remove_socket(self, socket):
    socket_thread = self.socket_threads.get(socket)
    if socket_threads:
      del self.socket_threads[socket]
      socket_thread.stop()
    else:
      LOGGER.error("Couldn't remove socket %s", socket)
