from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess

from echomesh.base import Config
from echomesh.color import Client
from echomesh.expression import Expression
from echomesh.network.Server import Server
from echomesh.util import Log
from echomesh.util import Subprocess
from echomesh.base import Quit

LOGGER = Log.logger(__name__)

class ClientServer(Server):
  INSTANCE = None

  def __init__(self):
    LOGGER.debug('Creating ClientServer')
    ClientServer.INSTANCE = self
    self.process = None
    self.constructed = False
    Config.add_client(self)
    Quit.register_atexit(self.kill)

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
        debug=config['debug'],
        read_callback=self.read_callback,
        timeout=Expression.convert(config['timeout']),
        )
      self.start()

    if (not self.process) and config['start']:
      args = {}
      if config['pipe_stdin']:
        args['stdin'] = subprocess.PIPE
      if config['pipe_stdout']:
        args['stdout'] = subprocess.PIPE

      command = Client.make_command()
      LOGGER.debug("About to start client process: '%s'" % command)
      try:
        self.process = subprocess.Popen(command, **args)
      except:
        LOGGER.error("Couldn't start the subprocess with command '%s'", command)
      else:
        LOGGER.debug("Client process started!")
    elif self.process:
      LOGGER.debug('Not starting client: the configuration said not to.')

  def read_callback(self, data):
    t = data.get('type')
    if t == 'hide':
      Config.assign(['light.visualizer.show=false'])

    elif t == 'midi':
      LOGGER.info('MIDI! %s', data)

    elif t == 'move':
      Config.assign(['light.visualizer.top_left=%s' % data['top_left']])

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
