from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Log
from echomesh.util.thread import Openable
from echomesh.util.thread import Locker

LOGGER = Log.logger(__name__)

class Closer(Openable.Openable):
  def __init__(self, parent=None):
    super(Closer, self).__init__(parent=parent)
    self.openables = []
    self.lock = Locker.Lock()

  def _add(self, openables, is_mutual):
    with Locker.Locker(self.lock):
      for o in openables:
        if o:
          self.openables.append(o)
          if is_mutual:
            o.group = self

  def add_openable(self, *openables):
    return self._add(openables, False)

  def add_openable_mutual(self, *openables):
    return self._add(openables, True)

  def start(self):
    super(Closer, self).start()
    with Locker.Locker(self.lock):
      for o in self.openables:
        o.start()

  def close(self):
    if not self.is_open:
      return
    with Locker.Locker(self.lock):
      super(Closer, self).close()
      for o in self.openables:
        try:
          o.close()
        except:
          LOGGER.error("Couldn't close %s" % o)
      self.openables = []

  def join(self):
    super(Closer, self).join()
    with Locker.Locker(self.lock):
      for c in self.openables:
        try:
          c.join()
        except:
          pass

class _ExitCloser(Closer):
  pass

EXIT_CLOSER = _ExitCloser()

def close_on_exit(to_close):
  EXIT_CLOSER.add_closer(to_close)

def on_exit():
  EXIT_CLOSER.close()
