from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import Config
from echomesh.base import Name
from echomesh.element import Load
from echomesh.element import Make
from echomesh.util import Log
from echomesh.util.thread.MasterRunnable import MasterRunnable

LOGGER = Log.logger(__name__)

class OldScore(MasterRunnable):
  def __init__(self, scorefile, parent=None):
    super(OldScore, self).__init__()
    self.parent = parent
    self.handlers = {}
    data = Load.load(scorefile)
    if not data:
      raise Exception('Unable to open score file %s' % scorefile)
    self.elements = Load.make(self, data)
    LOGGER.info('Loaded score "%s"', scorefile)
    self.add_slave(*self.elements)

  def add_handler(self, event_type, handler):
    self.handlers[event_type] = handler

  # TODO: where does this code go?
  def receive_event(self, event):
    event_type = event.get('event_type', None)
    if event_type:
      for handler in self.handlers.get(event_type, []):
        handler.handle(event)
    else:
      LOGGER.error('No event_type in event %s', event)


def make_score():
  score = OldScore(Config.get('score', 'file'))
  score.start()
  return score

"""

When a handler starts, it goes up the parent tree until it finds a parent with
an add_handler method, stores that parent, and then calls the method.

When the handler ends, it

"""
