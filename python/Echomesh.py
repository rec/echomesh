from __future__ import absolute_import, division, print_function, unicode_literals

import contextlib
import os.path
import threading
import time
import traceback

from command import Functions
from command import Processor
from command import Router
from command.Score import Score
from config import Config
from graphics import Display
from graphics import Tasks
from network import Clients
from network import Discovery
from sound import Microphone
from util import File
from util import Log
from util import Openable

DEFAULT_RULES = '~/echomesh/score/rules.yml'

LOGGER = Log.logger(__name__)

class Echomesh(Openable.Openable):
  def __init__(self):
    Openable.Openable.__init__(self)
    self.config = Config.CONFIG
    self.clients = Clients.Clients(self)
    callbacks = Router.router(self, self.clients)
    self.discovery = Discovery.Discovery(self.config, callbacks)
    self.process = Processor.process
    self.display = Display.display(self, self.config)

    def mic_events(*args):
      pass  # TODO
    self.mic_thread = Microphone.Microphone(self.config, mic_events)
    rules_file = self.config.get('rules', DEFAULT_RULES)
    rules = File.yaml_load_all(rules_file)
    self.score = Score(rules, Functions.functions(self.display))

  def send(self, data):
    self.discovery.send(data)

  def run(self):
    with contextlib.closing(self):
      try:
        self._run()
      except:
        LOGGER.critical(traceback.format_exc())

  def _run(self):
    self.discovery.start()
    self.clients.start()
    self.mic_thread.start()

    control_program = self.config.get('control_program', False)
    dconf = self.config['display']
    display_threaded = dconf.get('threaded', False)
    if display_threaded or not self.display:
      self.display and self.display.start()
      if control_program:
        self._keyboard_input()

    else:
      if control_program:
        threading.Thread(target=self._keyboard_input).start()
      self.display.loop()  # Blocks until complete


  def _keyboard_input(self):
    sleep = self.config.get('opening_sleep', 0.5)
    if sleep:
      time.sleep(sleep)

    while self.is_open:
      if not self.process(raw_input('echomesh: ').strip(), self):
        self.close()

  def close(self):
    if self.is_open:
      Openable.Openable.close(self)
      LOGGER.info('echomesh closing')
      self.discovery.close()
      self.mic_thread.close()
      self.display and self.display.close()
      self.score.close()
      self._join()

  def _join(self):
    self.display and self.display.join()
    self.discovery.join()
    self.mic_thread.join()
    self.score.join()

if __name__ == '__main__':
  Echomesh().run()
