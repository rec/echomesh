from __future__ import absolute_import, division, print_function, unicode_literals

import re

from echomesh.base import Config
from echomesh.element import Element
from echomesh.element import Load
from echomesh.util.thread import MasterRunnable

class Score(Element.Element):
  def __init__(self, parent, description):
    self.handlers = {}

    super(Score, self).__init__(parent, description)
    self.elements = Load.make(self, description['elements'])
    self.add_slave(*self.elements)
    self.name = ''

  def add_handler(self, handler, *types):
    for t in types or [handler['event_type']]:
      handlers = self.handlers.get(t, None)
      if handlers:
        handlers.add(handler)
      else:
        self.handlers[t] = {handler}

  def remove_handler(self, handler, *types):
    for t in types or [handler['event_type']]:
      self.handlers.get(t, set()).discard(handler)

  def handle(self, event):
    for handler in self.handlers.get(event['type'], []):
      handler.handle(event)

def make_score(scorefile):

Element.register(Score)

class Scores(MasterRunnable.MasterRunnable):
  MATCH_NAME = re.compile(r'(.*)\.(\d+)$')

  def __init__(self):
    super(Scores, self).__init__()
    self.scores = {}

  def start(self):
    self.is_running = True

  def make_score(self, scorefile):
    elements = Load.load(scorefile)
    if not elements:
      raise Exception('Unable to open score file %s' % scorefile)
    description = {'elements': elements, 'type': 'score'}
    score = Score(None, description)
    name = self._make_name(scorefile)
    self.scores[name] = score
    score.name = name
    return score

  def _make_name(self, scorefile):
    while scorefile in self.elements:
      match = MATCH_NAME.match(scorefile)
      if match:
        base, suffix = match.groups()
        suffix = str(1 + int(suffix))
      else:
        base, suffix = score_file, '0'
      scorefile = '%s.%d' % (base, suffix)

    return scorefile

