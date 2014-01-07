from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import time

from echomesh.util import Log

LOGGER = Log.logger(__name__)

def run_after(callback, t):
  def run():
    time.sleep(t)
    callback()

  thread = threading.Thread(target=callback, name='run_after')
  thread.daemon = True
  thread.start()
