"""An instance of echomesh, representing one node."""

from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.base import Config
from echomesh.base import Quit
from echomesh.element import ScoreMaster
from echomesh.expression import Expression
from echomesh.graphics import Display
from echomesh.light import LightSingleton
from echomesh.network import PeerSocket
from echomesh.network import Peers
from echomesh.output import pause_outputs
from echomesh.util import CLog
from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util.thread.RunAfter import run_after

LOGGER = Log.logger(__name__)

USE_KEYBOARD_THREAD = False

def test_str(s):
  LOGGER.info('test_str %s', s)

class Instance(MasterRunnable):
  def __init__(self):
    super(Instance, self).__init__()

    CLog.initialize()
    self.score_master = ScoreMaster.ScoreMaster()
    self.peers = Peers.Peers(self)
    self.socket = PeerSocket.PeerSocket(self, self.peers)
    self.callback = self.after_server_starts

    self.display = Display.display(self.callback)
    self.using_cechomesh = hasattr(self.display, 'callback')
    self.keyboard = self.osc = None
    if Config.get('control_program'):
      from echomesh.util.thread import Keyboard
      args = {}
      keyboard, self.keyboard = Keyboard.keyboard(
        self, new_thread=USE_KEYBOARD_THREAD or self.display)

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
    self.timeout = Config.get('network', 'timeout')

    def do_quit():
      LightSingleton.pause()
      pause_outputs()
      self.pause()
      self.unload()

    Quit.register_atexit(do_quit)

  def keyboard_callback(self, s):
    self.keyboard_queue.put(s)

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

  def display_loop(self):
    self.display.loop()
    if self.keyboard.thread:
      self.keyboard.thread.join()

  def main(self):
    if self.using_cechomesh:
      self.display_loop()
    else:
      self.after_server_starts()
    time.sleep(self.timeout)
    # Prevents crashes if you start and stop echomesh very fast.

  def after_server_starts(self):
    if self.using_cechomesh:
      run_after(self.run, Expression.convert(Config.get('delay_before_run')))
    else:
      self.run()
      if self.display:
        self.display_loop()
      elif not USE_KEYBOARD_THREAD and self.keyboard:
        self.keyboard.loop()
      else:
        while self.is_running:
          time.sleep(self.timeout)

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

