from __future__ import absolute_import, division, print_function, unicode_literals

import select

from echomesh.network.SocketThread import SocketThread
from echomesh.util import Log
from echomesh.util.thread import ThreadLoop

LOGGER = Log.logger(__name__)

TIMEOUT = 0.100

class SelectLoop(ThreadLoop.ThreadLoop):
  def __init__(self, *socket_threads):
    super(SelectLoop, self).__init__()
    # Map Python sockets to our data sockets
    self.socket_threads = list(socket_threads)

  def single_loop(self):
    sockets = [st.socket.socket for st in self.socket_threads]
    try:
      result = select.select(self.sockets, [], [], TIMEOUT)
    except:
      self.remove_bad()
    else:
      for socket in result[0]:
        for st in self.socket_threads:
          if st.socket.socket is socket:
            packet = socket.recv(BUFFER_SIZE)
            if packet:
              st.queue.put(packet)
            else:
              LOGGER.error('A socket %s was closed.', str(socket))
              self.remove_socket(st)

  def remove_bad(self):
    bad = []
    for st in self.socket_threads:
      try:
        select.select([st.socket.socket], [], [], timeout=0)
      except:
        bad.append(st)

    if bad:
      for st in bad:
        LOGGER.error('A socket %s went bad.', str(st))
        self.remove_socket(st)
    else:
      LOGGER.error('Tried to remove_bad, but found none.')

  def remove_socket(self, st):
    self.socket_threads.remove(st)
    st.stop()
