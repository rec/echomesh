from __future__ import absolute_import, division, print_function, unicode_literals

import threading
import traceback

from echomesh.util import Log
from echomesh.util.thread.RunnableOwner import RunnableOwner

LOGGER = Log.logger(__name__)

class ThreadLoop(RunnableOwner):
  def __init__(self, target=None, name=None,
               report_errors_when_closed=False):
    super(ThreadLoop, self).__init__()
    self.name = name or repr(self)
    has_target = getattr(self, 'target', None)
    self.report_errors_when_closed = report_errors_when_closed
    if target:
      assert not has_target
      self.target = target
    else:
      assert has_target

  def run(self):
    if not self.is_running:
      super(ThreadLoop, self).run()

      def loop_target():
        try:
          while self.is_running:
            self.target()
          LOGGER.debug('Loop for "%s" has finished', self.name)
        except:
          if self.is_running or self.report_errors_when_closed:
            LOGGER.critical(traceback.format_exc())
          self.close()
      self.thread = threading.Thread(target=loop_target)
      self.thread.start()

  def join(self):
    super(ThreadLoop, self).join()
    LOGGER.debug('Thread join for "%s"', self.name)
    try:
      self.thread.join()
    except:
      pass  # Swallow errors!  TODO

