"""An instance of echomesh, representing one node."""

from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.Cechomesh import cechomesh
from echomesh.base import Settings
from echomesh.base import Quit
from echomesh.element import ScoreMaster
from echomesh.expression import Expression
from echomesh.graphics import Display
from echomesh.util.hardware import GPIO
from echomesh.network import PeerSocket
from echomesh.network import Peers
from echomesh.output.Registry import pause_outputs
from echomesh.util import CLog
from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable
from echomesh.util.thread.RunAfter import run_after

LOGGER = Log.logger(__name__)

USE_KEYBOARD_THREAD = False

class Instance(MasterRunnable):
    def __init__(self):
        super(Instance, self).__init__()

        def do_quit():
            pause_outputs()
            self.pause()
            self.unload()

        Quit.register_atexit(do_quit)
        gpio = Settings.get('hardware', 'gpio')
        if gpio['enable']:
            GPIO.on_gpio(Quit.request_quit,
                         gpio['shutdown_pin'],
                         gpio['shutdown_pin_pull_up'],
                         gpio['shutdown_pin_bounce_time'])

        CLog.initialize()
        self.score_master = ScoreMaster.ScoreMaster()
        self.peers = Peers.Peers(self)
        self.socket = PeerSocket.PeerSocket(self, self.peers)
        # self.callback = self.after_server_starts

        self.display = Display.display(self.callback)
        self.keyboard_runnable = self.osc = None
        if Settings.get('control_program'):
            from echomesh.util.thread import Keyboard
            args = {}
            keyboard, self.keyboard_runnable = Keyboard.keyboard(
              self, new_thread=USE_KEYBOARD_THREAD or self.display)

        osc_client = Settings.get('osc', 'client', 'enable')
        osc_server = Settings.get('osc', 'server', 'enable')
        if osc_client or osc_server:
            from echomesh.sound.Osc import Osc
            self.osc = Osc(osc_client, osc_server)

        self.add_mutual_pause_slave(
            self.socket, self.keyboard_runnable, self.osc)
        self.add_slave(self.score_master)
        self.add_slave(self.display)
        self.set_broadcasting(False)
        self.timeout = Settings.get('network', 'timeout')

    def keyboard_callback(self, s):
        self.keyboard_runnable_queue.put(s)

    def broadcasting(self):
        return self._broadcasting

    def set_broadcasting(self, b):
        self._broadcasting = b
        if self.keyboard_runnable:
            self.keyboard_runnable.alert_mode = b

    def send(self, **data):
        self.socket.send(data)

    def handle(self, event):
        return self.score_master.handle(event)

    def display_loop(self):
        self.display.loop()
        thread = getattr(self.keyboard_runnable, 'thread', None)
        thread and thread.join()

    def main(self):
        if cechomesh.LOADED:
            self.display_loop()
        else:
            self.after_server_starts()
        time.sleep(self.timeout)
        # Prevents crashes if you start and stop echomesh very fast.

    def callback(self, data):
        if data == 'start':
            self.after_server_starts()
        else:
            print(data)

    def after_server_starts(self):
        if cechomesh.LOADED:
            run_after(self.run,
                      Expression.convert(Settings.get('delay_before_run')))
        else:
            self.run()
            if self.display:
                self.display_loop()
            elif not USE_KEYBOARD_THREAD and self.keyboard_runnable:
                self.keyboard_runnable.loop()
            else:
                while self.is_running:
                    time.sleep(self.timeout)
