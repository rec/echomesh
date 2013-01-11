from __future__ import absolute_import, division, print_function, unicode_literals

import contextlib
import os
import os.path
import sys
import threading
import time
import traceback

from echomesh.command import Processor
from echomesh.command import Score

from echomesh.config import Config

from echomesh.graphics import Display

from echomesh.network import PeerSocket

from echomesh.sound import Microphone
from echomesh.sound import SetOutput

from echomesh.util import Log

from echomesh.util.file import File

from echomesh.util.thread import Closer
from echomesh.util.thread import Keyboard

LOGGER = Log.logger(__name__)
ECHOMESH = None
MESSAGE = """
           echomesh
Type help for a list of commands

"""

def _make_keyboard(echomesh):
  if Config.is_control_program:
      processor = lambda x: Processor.process(x, echomesh)
      keyboard =  Keyboard.Keyboard(parent=echomesh,
                                    sleep=Config.get('opening_sleep'),
                                    message=MESSAGE,
                                    processor=processor)

class Echomesh(Closer.Closer):
  INSTANCE = None

  def __init__(self):
    super(Echomesh, self).__init__()
    if Echomesh.INSTANCE:
      LOGGER.error('There is more than one instance of Echomesh')
    else:
      Echomesh.INSTANCE = self

    socket = PeerSocket.PeerSocket(self)
    score = Score.make_score()

    self.send = socket.send
    self.receive = score.receive_event

    self.add_openable_mutual(socket,
                             _make_keyboard(self),
                             Display.display(self),
                             Microphone.Microphone(self._mic_event),
                             score)

  def _mic_event(self, level):
    self.send(type='event', event='mic', key=level)

  # TODO: these next methods don't work any more.
  def remove_local(self):
    try:
      Config.remove_local()
      self.microphone.set_config()

    except OSError as e:
      LOGGER.warn("No local file %s" % Config.LOCAL_CHANGED_FILE)

    try:
      os.remove(LOCAL_SCORE)
    except OSError as e:
      LOGGER.warn("No local score file %s", LOCAL_SCORE)

  def set_config(self, config):
    Config.change(config)
    self.microphone.set_config()

  def set_score(self, score):
    File.yaml_dump_all(LOCAL_SCORE, score)
    self.score.set_score(score)


if __name__ == '__main__':
  if Config.get('autostart') or len(sys.argv) < 2 or sys.argv[1] != 'autostart':
    SetOutput.set_output(Config.get('audio', 'output', 'route'))
    Echomesh().start()
    Closer.on_exit()
  else:
    LOGGER.info("Not autostarting because autostart=False")
