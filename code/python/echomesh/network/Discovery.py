from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import errno
import socket
import threading

from echomesh.config import Config
from echomesh.network import Address
from echomesh.network import DataSocket
from echomesh.util import Closer
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Discovery(Closer.Closer):
  DOCUMENT_START = '---\n'
  DOCUMENT_END = '....\n'

  def __init__(self, callbacks):
    super(Discovery, self).__init__()
    self.callbacks = callbacks

  def start(self):
    port = Config.get('discovery', 'port')
    try:
      self._receive = DataSocket.Receive(port, self.callbacks)
      self.mutual_closer(self._receive)

      self._send = DataSocket.Send(port)
      self.mutual_closer(self._send)

    except socket.error as e:
      if e.errno == errno.EADDRINUSE:
        LOGGER.error('An echomesh node is already running on this machine')
        self.close()
        return False
      else:
        raise

    self._receive.start()
    self._send.start()
    LOGGER.info('Started discovery on port %d', port)
    return True

  def send(self, **data):
    if 'source' not in data:
      data = dict(**data)
      data['source'] = Address.NODENAME
    self._send.send(data)

  def join(self):
    try:
      self._receive.join()
    except:
      pass

    try:
      self._send.join()
    except:
      pass

  def _error(self, data):
    LOGGER.error('No callbacks for type %s', data['type'])
