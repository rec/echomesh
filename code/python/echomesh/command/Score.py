from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import Config
from echomesh.base import Name
from echomesh.element import Load
from echomesh.element import Make
from echomesh.util import Log
from echomesh.util.thread.RunnableOwner import RunnableOwner

LOGGER = Log.logger(__name__)

class Score(RunnableOwner):
  def __init__(self, scorefile, parent=None):
    super(Score, self).__init__()
    self.parent = parent
    self.handlers = {}
    data = Load.load(scorefile)
    if not data:
      raise Exception('Unable to open score file %s' % scorefile)
    self.elements = Load.make(self, *data)

  def add_handler(self, event_type, handler):
    self.handlers[event_type] = handler

  def receive_event(self, event):
    event_type = event.get('subtype', None)
    if event_type:
      for handler in self.handlers.get(event_type, []):
        handler.handle(event)
    else:
      LOGGER.error('No event_type in event %s', event)


def make_score():
  score = Score(Config.get('score', 'file'))
  score.run()
  return score

