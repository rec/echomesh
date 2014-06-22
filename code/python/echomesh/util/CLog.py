from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh import cechomesh

from echomesh.base import Config
from echomesh.util import Log


LOGGER = Log.logger(__name__)

class _Redirector(object):
  def __init__(self):
    self.redirecting = False

  def config_update(self, get):
    if get('logging', 'redirect_glog') != self.redirecting:
      self.redirecting = not self.redirecting

      if cechomesh.LOADED:
        for i, level in enumerate(('info', 'warning', 'error', 'error')):
          cechomesh.set_logger(i, self.redirecting and getattr(LOGGER, level))

def initialize():
  cechomesh.LOADED and cechomesh.init_log()
  Config.add_client(_Redirector())
