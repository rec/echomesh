from __future__ import absolute_import, division, print_function, unicode_literals

import os.path

from echomesh.base import Config
from echomesh.element import Load
from echomesh.base import Name
from echomesh.util import Log
from echomesh.util.thread import Closer

LOGGER = Log.logger(__name__)

class Score(Closer.Closer):
  def __init__(self, scorefile, parent=None):
    super(Score, self).__init__()
    self.parent = parent
    self.handlers = {}
    self.elements = Load.load_and_make(self, scorefile)

    if self.elements is None:
      raise Exception('Unable to open score file %s' % scorefile)

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
  score.start()
  return score

