from __future__ import absolute_import, division, print_function, unicode_literals

import contextlib
import os
import os.path
import sys
import threading
import time
import traceback

from command import Processor
from command import Router
from config import Config
from graphics import Display
from network import Clients
from network import Discovery
from sound import Microphone
from sound import SetOutput
from util import File
from util import Log
from util.Openable import Openable
from util.Closer import Closer

DEFAULT_SCORE = '~/echomesh/score/score.yml'
LOCAL_SCORE = os.path.expanduser('~/.echomesh-score')

LOGGER = Log.logger(__name__)

class Echomesh(Openable):
  def __init__(self):
    Openable.__init__(self)
    self.config = Config.CONFIG
    self.autostart = (self.config.get('autostart', True) or len(sys.argv) < 2 or
                      sys.argv[1] != 'autostart')

    if not self.autostart:
      return

    self.clients = Clients.Clients(self)
    callbacks = Router.router(self, self.clients)
    self.discovery = Discovery.Discovery(self.config, callbacks)
    self.process = Processor.process
    self.display = Display.display(self, self.config)
    self.closer = Closer()

    SetOutput.set_output(self.config.get('audio', {}).get('route', None))
    self.microphone = Microphone.Microphone(self.config, self._mic_event)
    self.control_program = Config.is_control_program()

    self.load_score()

  def load_score(self):
    if Config.is_enabled('score'):
      from command.Score import Score
      from command import Functions

      score = File.yaml_load_all(LOCAL_SCORE)
      if not score:
        score_file = self.config.get('score', DEFAULT_SCORE)
        score = File.yaml_load_all(score_file)
      self.score = Score(score, Functions.functions(self, self.display))
    else:
      self.score = Openable()

  def remove_local(self):
    try:
      Config.remove_local()
      self.config = Config.CONFIG
      self.microphone.set_config(self.config)

    except OSError as e:
      LOGGER.warn("No local file %s" % Config.LOCAL_CHANGED_FILE)

    try:
      os.remove(LOCAL_SCORE)
      self.load_score()
    except OSError as e:
      LOGGER.warn("No local score file %s", LOCAL_SCORE)

  def send(self, **data):
    self.discovery.send(**data)

  def receive_event(self, event):
    self.score.receive_event(event)

  def set_score(self, score):
    File.yaml_dump_all(LOCAL_SCORE, score)
    self.score.set_score(score)

  def add_closer(self, closer):
    self.closer.add_closer(closer)

  def set_config(self, config):
    Config.change(config)
    self.microphone.set_config(config)

  def run(self):
    if self.autostart:
      with contextlib.closing(self):
        try:
          self._run()
        except:
          LOGGER.critical(traceback.format_exc())
    else:
      LOGGER.info("Not autostarting because autostart = False")

  def _mic_event(self, level):
    self.send(type='event', event='mic', key=level)

  def _run(self):
    self.discovery.start()
    self.clients.start()
    self.microphone.start()

    dconf = self.config['display']
    display_threaded = dconf.get('threaded', False)
    if display_threaded or not self.display:
      self.display and self.display.start()
      if self.control_program:
        self._keyboard_input()

    else:
      if self.control_program:
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
      Openable.close(self)
      LOGGER.info('echomesh closing')
      self.discovery.close()
      self.closer.close()
      self.microphone.close()
      self.display and self.display.close()
      self.score.close()
      self._join()

  def _join(self):
    self.display and self.display.join()
    self.discovery.join()
    self.microphone.join()
    self.score.join()

if __name__ == '__main__':
  Echomesh().run()
