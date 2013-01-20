from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from echomesh.base import Config
Config.recalculate(*sys.argv)

from echomesh.command import Score
from echomesh.graphics import Display
from echomesh.network import PeerSocket
from echomesh.sound import Microphone
from echomesh.sound import SetOutput
from echomesh.util import Log
from echomesh.util.thread import Closer
from echomesh.util.thread import Keyboard

LOGGER = Log.logger(__name__)

class Echomesh(Closer.Closer):
  INSTANCE = None

  def __init__(self):
    super(Echomesh, self).__init__()
    if Echomesh.INSTANCE:
      LOGGER.error('There is more than one instance of Echomesh')
    else:
      Echomesh.INSTANCE = self

    self.socket = PeerSocket.PeerSocket(self)
    self.score = Score.make_score()

    self.add_openable_mutual(self.socket,
                             Keyboard.keyboard(self),
                             Display.display(self),
                             Microphone.microphone(self._mic_event),
                             self.score)

  def send(self, **data):
    self.socket.send(data)

  def receive(self, event):
    return self.score.receive_event(event)

  def start(self):
    super(Echomesh, self).start()
    self.join()

  def _mic_event(self, level):
    self.send(type='event', event_type='mic', key=level)

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
    from echomesh.base import File
    File.yaml_dump_all(LOCAL_SCORE, score)
    self.score.set_score(score)

def startup():
  if Config.get('autostart') or len(sys.argv) < 2 or sys.argv[1] != 'autostart':
    SetOutput.set_output(Config.get('audio', 'output', 'route'))
    return True

def shutdown():
  if Config.get('dump_unused_configs'):
    import yaml
    print(yaml.safe_dump(Config.get_unvisited()))
  Closer.on_exit()

if __name__ == '__main__':
  if startup():
    Echomesh().start()
    shutdown()
  else:
    LOGGER.info("Not autostarting because autostart=False")
