from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

from echomesh.base import Config
from echomesh.color import Client
from echomesh.expression import Units
from echomesh.network.Server import Server
from echomesh.util import Log
from echomesh.util import Subprocess
from echomesh.util import Quit

LOGGER = Log.logger(__name__)

class ClientServer(Server):
  INSTANCE = None

  def __init__(self):
    LOGGER.debug('Creating ClientServer')
    ClientServer.INSTANCE = self
    self.process = None
    self.constructed = False
    Config.add_client(self)
    Quit.register(self.kill)

  def config_update(self, get):
    config = get('network', 'client')
    if self.constructed:
      # TODO: restart the server on the fly if its parameters change.
      pass
    else:
      self.constructed = True
      super(ClientServer, self).__init__(
        config['host_name'],
        config['port'],
        allow_reuse_address=config['allow_reuse_address'],
        read_callback=self.read_callback,
        timeout=Units.convert(config['timeout']),
        )
      self.start()

    if (not self.process) and config['start']:
      args = {}
      if config['pipe_stdin']:
        args['stdin'] = subprocess.PIPE
      if config['pipe_stdout']:
        args['stdout'] = subprocess.PIPE
      LOGGER.debug("About to start client process")
      self.process = subprocess.Popen(Client.make_command(), **args)
      LOGGER.debug("Client process started!")
    else:
      LOGGER.debug("Didn't start client process")

  def read_callback(self, data):
    t = data.get('type')
    if t == 'hide':
      Config.assign(['light.vis.show=false'])

    elif t == 'midi':
      LOGGER.info('MIDI! %s', data)

    elif t == 'move':
      Config.assign(['light.vis.top_left=%s' % data['top_left']], False)

  def kill(self):
    try:
      self.process.terminate()
    except:
      pass
    try:
      self.process.kill()
    except:
      pass
    try:
      Subprocess.run(Client.KILL_COMMAND)
    except:
      pass
    try:
      self.pause()
    except:
      pass

def instance():
  return ClientServer.INSTANCE or (not Quit.QUITTING and ClientServer())
