from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from echomesh.base import Config
from echomesh.command import Score
from echomesh.graphics import Display
from echomesh.network import PeerSocket
from echomesh.sound import Microphone
from echomesh.util import Log
from echomesh.util.thread import Keyboard
from echomesh.util.thread.RunnableOwner import RunnableOwner

LOGGER = Log.logger(__name__)

class Echomesh(RunnableOwner):
  INSTANCE = None

  def __init__(self):
    super(Echomesh, self).__init__()
    if Echomesh.INSTANCE:
      LOGGER.error('There is more than one instance of Echomesh')
    else:
      Echomesh.INSTANCE = self

    self.socket = PeerSocket.PeerSocket(self)
    self.peers = self.socket.peers
    self.score = Score.make_score()

    self.add_mutual_stop_slave(self.socket,
                               Keyboard.keyboard(self),
                               Display.display(self),
                               Microphone.microphone(self._mic_event))
    self.add_slave(self.score)

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
