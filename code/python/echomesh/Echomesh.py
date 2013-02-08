from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from echomesh.base import Config
from echomesh.element import Make
from echomesh.element import ScoreMaster
from echomesh.graphics import Display
from echomesh.network import PeerSocket
from echomesh.sound import Microphone
from echomesh.util import Log
from echomesh.util.thread import Keyboard
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

class Echomesh(MasterRunnable):
  INSTANCE = None

  def __init__(self):
    super(Echomesh, self).__init__()
    if Echomesh.INSTANCE:
      LOGGER.error('There is more than one instance of Echomesh')
    else:
      Echomesh.INSTANCE = self

    self.socket = PeerSocket.PeerSocket(self)
    self.peers = self.socket.peers
    self.score_master = ScoreMaster.ScoreMaster()
    scorefile = Config.get('score', 'file')
    if scorefile:
      self.score_master.start_score(scorefile)

    self.display = Display.Display()
    mic = Microphone.microphone(self._mic_event)
    kbd = Keyboard.keyboard(self)

    self.add_mutual_stop_slave(self.socket, kbd, mic)
    self.add_slave(self.score_master, self.display)

  def send(self, **data):
    self.socket.send(data)

  def receive_event(self, event):
    return self.score.receive_event(event)

  def _mic_event(self, level):
    self.send(type='event', event_type='mic', key=level)

  def set_score(self, score):
    from echomesh.base import File
    File.yaml_dump_all(LOCAL_SCORE, score)
    self.score.set_score(score)

  def _on_start(self):
    self.display.loop()
