from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import errno
import threading

from echomesh.config import Config
from echomesh.network import DataSocket
from echomesh.util import Closer
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Discovery(Closer.Closer):
  def __init__(self, callbacks):
    super(Discovery, self).__init__()
    self.callbacks = callbacks

  def start(self):
    timeout = Config.get('discovery', 'timeout')
    port = Config.get('discovery', 'port')
    self.data_socket = DataSocket.data_socket(port, timeout, self.callbacks)
    if not self.data_socket:
      self.close()
      return False

    self.mutual_closer(self.data_socket)
    self.data_socket.start()

    LOGGER.info('Started discovery on port %d', port)
    return True

