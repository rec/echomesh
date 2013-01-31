from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.element import Element
from echomesh.element import Load

class Score(Element.Element):
  def __init__(self, parent, description):
    self.handlers = {}

    super(Score, self).__init__(parent, description)
    self.elements = Load.make(self, description['elements'])
    self.add_slave(*self.elements)

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

def make_score():
  scorefile = Config.get('score', 'file')
  elements = Load.load(scorefile)
  if not elements:
    raise Exception('Unable to open score file %s' % scorefile)
  description = {'elements': elements, 'type': 'score'}
  return Score(None, description)

Element.register(Score)
