from __future__ import absolute_import, division, print_function, unicode_literals

import time

import cechomesh

from echomesh.util.thread.Runnable import Runnable

class CDisplay(Runnable):
  def __init__(self, callback=None):
    super(CDisplay, self).__init__()
    self.callback = callback

  def _on_pause(self):
    cechomesh.stop_application()

  def loop(self):
    print('starting cechomesh')
    cechomesh.start_application(self.callback)
