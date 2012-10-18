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
from util import Log
from util import Openable

IMAGE = '/development/echomesh/data/ball.gif'

LOGGER = Log.logger(__name__)

class Echomesh(Openable.Openable):
  def __init__(self):
    Openable.Openable.__init__(self)
    self.config = Config.CONFIG
    self.discovery = Discovery.Discovery(self.config)
    self.clients = Clients.Clients(self.discovery)
    self.router = Router.router(self, self.config, self.clients)
    self.discovery.callbacks = self.router
    self.display = Display.Display(self.config)
    self.control_loop = ControlLoop.ControlLoop(self.config, self.display.clock)
    self.mic_thread = Microphone.run_mic_levels_thread(print, self.config)

  def run(self):
    with closing(self):
      self.discovery.start()
      self.display.start()
      self._add_tasks()
      self.control_loop.start()
      self.mic_thread.start()

      if self.config.get('control_program', False):
        while self.is_open:
          if not self._process_command(raw_input('echomesh: ')):
            self.close()

      else:
        self._join()

  def close(self):
    if self.is_open:
      Openable.Openable.close(self)
      LOGGER.info('echomesh closing')
      self.discovery.close()
      self.mic_thread.close()
      self.display.close()
      self.control_loop.close()
      self._join()

  def _join(self):
    self.discovery.join()
    self.mic_thread.join()
    self.control_loop.join()

  def _add_tasks(self):
    p = ImagePath.ImagePath(IMAGE, 45, 10.0, self.display)
    self.control_loop.tasks = [Tasks.Clearer(self.display), p,
                               Tasks.Quitter(), Tasks.Flipper()]

  def _process_command(self, command):
    return command != 'quit'

if __name__ == '__main__':
  Echomesh().run()
