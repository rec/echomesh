"""An instance of echomesh, representing one node."""

from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.base import Config
from echomesh.color import LightSingleton
from echomesh.element import ScoreMaster
from echomesh.graphics import Display
from echomesh.network import PeerSocket
from echomesh.network import Peers
from echomesh.util import Log
from echomesh.util import Quit
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

class Instance(MasterRunnable):
  def __init__(self):
    super(Instance, self).__init__()

    self.score_master = ScoreMaster.ScoreMaster()
    self.peers = Peers.Peers(self)
    self.socket = PeerSocket.PeerSocket(self, self.peers)

    self.display = Display.Display()
    if Config.get('control_program', 'enable'):
      from echomesh.util.thread import Keyboard
      self.keyboard = Keyboard.keyboard(self)
    else:
      self.keyboard = None

    self.add_mutual_pause_slave(self.socket, self.keyboard)
    self.add_slave(self.score_master)
    self.add_slave(self.display)
    self.set_broadcasting(False)
    self.mic = None
    Quit.register(self.pause)

  def _on_pause(self):
    super(Instance, self)._on_pause()
    LightSingleton.stop()

  def broadcasting(self):
    return self._broadcasting

  def set_broadcasting(self, b):
    self._broadcasting = b
    if self.keyboard:
      self.keyboard.alert_mode = b

  def send(self, **data):
    self.socket.send(data)

  def handle(self, event):
    return self.score_master.handle(event)

  def main(self):
    self.run()
    self.display.loop()
    self.keyboard.thread and self.keyboard.thread.join()
    time.sleep(0.1)  # Prevents crashes in shutdown.

  def start_mic(self):
    if not self.mic:
      from echomesh.sound import Microphone
      def mic_event(level):
        self.send(type='event', event_type='mic', key=level)

      self.mic = Microphone.microphone(mic_event)
      self.mic.run()
      self.add_mutual_pause_slave(self.mic)

  def stop_mic(self):
    if self.mic:
      self.mic.pause()
      self.remove_slave(self.mic)
      self.mic = None

INSTANCE = Instance()
main = INSTANCE.main
