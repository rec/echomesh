from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Name
from echomesh.expression import Expression
from echomesh.network import DataSocket
from echomesh.remote import Remote
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util import Log

LOGGER = Log.logger(__name__)

USE_YAML_SOCKET = True
DEFAULT_TIMEOUT = 0.1

class PeerSocketBase(MasterRunnable):
  def __init__(self, instance, peers, config_name):
    super(PeerSocketBase, self).__init__()
    self.instance = instance
    self.peers = peers
    self.config_name = config_name
    self.add_slave(self.peers)
    self.port = -1
    self.socket = None
    Config.add_client(self)

  def config_update(self, get):
    new_port = get('network', self.config_name, 'port')
    timeout_name = 'network', self.config_name, 'timeout'
    timeout = get(*timeout_name)
    self.port, old_port = new_port, self.port
    try:
      self.timeout = Expression.convert(timeout)
    except:
      timeout_name = '.'.join(timeout_name)
      LOGGER.error(
        '\nCouldn\'t evaluate value "%s" in "%s=%s"',
        timeout, timeout_name, timeout, raw=True)
      LOGGER.error(
        'Timeout defaults to %s=%s.', timeout_name, DEFAULT_TIMEOUT, raw=True)
      self.timeout = DEFAULT_TIMEOUT

    if self.is_running and self.socket:
      if self.port == old_port:
        self.socket.timeout = self.timeout
      else:
        self.remove_slave(self.socket)
        self.socket.pause()
        self._make_socket()

  def send(self, data):
    if self.is_running:
      data['source'] = Name.NAME
      self.socket.send(data)

  def _on_run(self):
    super(PeerSocketBase, self)._on_run()
    if not self.socket:
      self._make_socket()

  def _make_socket(self):
    self.socket = DataSocket.DataSocket(self.port, self.timeout, self.router)
    self.add_mutual_pause_slave(self.socket)
    self.socket.run()

  def router(self):
    pass

class PeerSocket(PeerSocketBase):
  def __init__(self, instance, peers):
    super(PeerSocket, self).__init__(instance, peers, 'discovery')

  def router(self, data):
    Remote.execute(self.instance, **data)

