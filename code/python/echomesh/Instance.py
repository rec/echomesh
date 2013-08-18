"""An instance of echomesh, representing one node."""

from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.base import Config
from echomesh.base import Quit
from echomesh.element import ScoreMaster
from echomesh.graphics import Display
from echomesh.light import LightSingleton
from echomesh.network import PeerSocket
from echomesh.network import Peers
from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

KEYBOARD_IN_THREAD = True

class Instance(MasterRunnable):
  def __init__(self):
    super(Instance, self).__init__()

    self.score_master = ScoreMaster.ScoreMaster()
    self.peers = Peers.Peers(self)
    self.socket = PeerSocket.PeerSocket(self, self.peers)

    self.display = Display.display()
    self.keyboard = self.osc = None
    if Config.get('control_program'):
      from echomesh.util.thread import Keyboard
      self.keyboard = Keyboard.keyboard(self,
                                        KEYBOARD_IN_THREAD or self.display)

    osc_client = Config.get('osc', 'client', 'enable')
    osc_server = Config.get('osc', 'server', 'enable')
    if osc_client or osc_server:
      from echomesh.sound.Osc import Osc
      self.osc = Osc(osc_client, osc_server)

    self.add_mutual_pause_slave(self.socket, self.keyboard, self.osc)
    self.add_slave(self.score_master)
    self.add_slave(self.display)
    self.set_broadcasting(False)
    self.mic = None
    Quit.register_atexit(self.pause)

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
    if self.display:
      self.display.loop()
      if self.keyboard.thread:
        self.keyboard.thread.join()
    elif not KEYBOARD_IN_THREAD and self.keyboard:
      self.keyboard.loop()
    else:
      while self.is_running:
        pass
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
