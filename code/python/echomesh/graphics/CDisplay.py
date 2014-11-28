from __future__ import absolute_import, division, print_function, unicode_literals

import time

from echomesh.Cechomesh import cechomesh

from echomesh.util import Log
from echomesh.util.thread.Runnable import Runnable

LOGGER = Log.logger(__name__)

class CDisplay(Runnable):
    def __init__(self, callback=None):
        super(CDisplay, self).__init__()
        self.callback = callback
        self.is_running = True

    def _on_pause(self):
        cechomesh.LOADED and cechomesh.stop_application()

    def loop(self):
        if cechomesh.LOADED:
            cechomesh.start_application(self.callback)
