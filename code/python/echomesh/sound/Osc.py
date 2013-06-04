from __future__ import absolute_import, division, print_function, unicode_literals

import OSC

from echomesh.base import Config
from echomesh.util import Log
from echomesh.util.thread.ThreadRunnable import ThreadRunnable

LOGGER = Log.logger(__name__)

class OscClient(ThreadRunnable):
  def __init__(self):
    self.client = None
    Config.add_client(self)

  def config_update(self, get):
    if self.client:
      return  # TODO: allow a restart

def make_osc(use_client, use_server):
  pass
