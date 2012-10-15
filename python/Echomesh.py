from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import closing

from command import Router
from config import Config
from network import Clients
from network import Discovery
from sound import Microphone

class Echomesh(object):
  def __init__(self):
    self.config = Config.config()
    self.discovery = Discovery.Discovery(self.config['discovery_port'],
                                         self.config['discovery_timeout'])
    self.clients = Clients.Clients(self.discovery)
    self.router = Router.router(self.config, self.clients)
    self.discovery.callbacks = self.router

  def run(self):
    self.discovery.start()
    mic_thread = Microphone.run_mic_levels_thread(print, self.config)
    with closing(self.discovery), closing(mic_thread):
      raw_input('Press return to exit\n')
    self.discovery.join()


if __name__ == '__main__':
  Echomesh().run()
