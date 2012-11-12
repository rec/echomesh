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

LOGGER = Log.logger(__name__)

class Echomesh(Closer):
  def __init__(self):
    super(Echomesh, self).__init__()
    self.autostart = (Config.get(['autostart'], True) or len(sys.argv) < 2 or
                      sys.argv[1] != 'autostart')

    if not self.autostart:
      return

    self.clients = Clients.Clients(self)
    callbacks = Router.router(self, self.clients)
    self.discovery = Discovery.Discovery(callbacks)
    self.process = Processor.process
    self.display = Display.display(self)

    SetOutput.set_output(Config.get(['audio', 'route']))
    self.microphone = Microphone.Microphone(self._mic_event)
    self.control_program = Config.is_control_program()

    self.load_score()

  def load_score(self):
    self.score_enabled = Config.is_enabled('score')
    if self.score_enabled:
      from command.Score import Score
      from command import Functions

      score = Config.get(['score', 'file'])
      functions = Functions.functions(self, self.display)
      self.score = Score(score, functions)
      self.score.start()
    else:
      self.score = Openable()

  def remove_local(self):
    try:
      Config.remove_local()
      self.microphone.set_config()

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
    if self.score_enabled:
      self.score.receive_event(event)
    else:
      LOGGER.info('Event: %(event)s, %(key)s', event)

  def set_score(self, score):
    File.yaml_dump_all(LOCAL_SCORE, score)
    self.score.set_score(score)

  def set_config(self, config):
    Config.change(config)
    self.microphone.set_config()

  def run(self):
    if self.autostart:
      with contextlib.closing(self):
        try:
          self._run()
        except:
          LOGGER.critical(traceback.format_exc())
    else:
      LOGGER.info("Not autostarting because autostart=False")

  def _mic_event(self, level):
    self.send(type='event', event='mic', key=level)

  def _run(self):
    if not self.discovery.start():
      LOGGER.error("Closing because Discovery didn't start")
      self.close()
      return

    self.clients.start()
    self.microphone.start()

    display_threaded = Config.get(['display', 'threaded'], False)
    if display_threaded or not self.display:
      self.display and self.display.start()
      if self.control_program:
        self._keyboard_input()
      self._join()

    else:
      if self.control_program:
        threading.Thread(target=self._keyboard_input).start()
      self.display.loop()  # Blocks until complete
    LOGGER.info('Finished Echomesh._run')

  def _keyboard_input(self):
    sleep = Config.get(['opening_sleep'], 0.5)
    if sleep:
      time.sleep(sleep)

    print()
    print('           echomesh')
    print()
    print('Type help for a list of commands')
    print()
    while self.is_open:
      if not self.process(raw_input('echomesh: ').strip(), self):
        self.close()

  def close(self):
    if self.is_open:
      LOGGER.info('closing')
      self.discovery.close()
      super(Echomesh, self).close()
      self.microphone.close()
      self.display and self.display.close()
      self.score.close()
      self._join()

  def _join(self):
    LOGGER.debug('joining')
    self.display and self.display.join()
    LOGGER.debug('display joined')
    self.discovery.join()
    LOGGER.debug('discovery joined')
    self.microphone.join()
    LOGGER.debug('mic joined')
    self.score.join()
    LOGGER.debug('joined')

if __name__ == '__main__':
  Echomesh().run()
