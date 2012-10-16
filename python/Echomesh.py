from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import closing

from command import Router
from config import Config
from network import Clients
from network import Discovery
from sound import Microphone

class Echomesh(object):
  def __init__(self):
    self.config = Config.CONFIG
    self.discovery = Discovery.Discovery(self.config)
    self.clients = Clients.Clients(self.discovery)
    self.router = Router.router(self, self.config, self.clients)
    self.discovery.callbacks = self.router

  def close(self):
    self.discovery.close()
    if hasattr(self, 'mic_thread'):
      self.mic_thread.close()
    self.discovery.join()

  def run(self):
    self.discovery.start()
    self.mic_thread = Microphone.run_mic_levels_thread(print, self.config)
    with closing(self):
      raw_input('Press return to exit\n')


if __name__ == '__main__':
  Echomesh().run()
