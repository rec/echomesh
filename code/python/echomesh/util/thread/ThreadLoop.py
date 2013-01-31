from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import traceback

from echomesh.util import Log
from echomesh.util.thread.ThreadRunnable import ThreadRunnable

LOGGER = Log.logger(__name__)

class ThreadLoop(ThreadRunnable):
  def __init__(self, single_loop=None, name=None, report_error=False):
    super(ThreadLoop, self).__init__(report_error=report_error)
    self.name = name or repr(self)
    self.single_loop = single_loop or self.single_loop
    assert self.single_loop

  def target(self):
    while self.is_running:
      self.single_loop()
