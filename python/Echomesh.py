from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import closing

from command import Router
from config import Config
from graphics import Display
from graphics import Tasks
from graphics import ImagePath
from network import Clients
from network import Discovery
from sound import Microphone
from util import ControlLoop

IMAGE = '/development/echomesh/data/ball.gif'

class Echomesh(object):
  def __init__(self):
    self.config = Config.CONFIG
    self.discovery = Discovery.Discovery(self.config)
    self.clients = Clients.Clients(self.discovery)
    self.router = Router.router(self, self.config, self.clients)
    self.discovery.callbacks = self.router
    self.control_loop = ControlLoop.ControlLoop(self.config)
    self.display = Display.Display(self.config)
    self.mic_thread = Microphone.run_mic_levels_thread(print, self.config)

  def run(self):
    with closing(self):
      self.discovery.start()
      self.display.start()
      self._add_tasks()
      self.control_loop.start()
      self.mic_thread.start()
      raw_input('Press return to exit\n')

  def close(self):
    self.discovery.close()
    self.mic_thread.close()
    self.display.close()
    self.control_loop.close()

    self.discovery.join()

  def _add_tasks(self):
    p = ImagePath.ImagePath(IMAGE, 45, 10.0, self.display)
    self.control_loop.tasks = [Tasks.Clearer(self.display), p,
                               Tasks.Quitter(), Tasks.Flipper()]

if __name__ == '__main__':
  Echomesh().run()
