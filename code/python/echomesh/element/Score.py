from __future__ import absolute_import, division, print_function, unicode_literals

import collections

from echomesh.base import Config
from echomesh.element import Element
from echomesh.element import Load

class Score(Element.Element):
  def __init__(self, parent, description):
    self.handlers = collections.defaultdict(set)

    super(Score, self).__init__(parent, description)
    self.elements = Load.make(self, description['elements'])
    self.add_slave(*self.elements)
    self.name = ''

  def add_handler(self, handler, *types):
    for t in (types or [handler['event_type']]):
      self.handlers[t].add(handler)

  def remove_handler(self, handler, *types):
    for t in (types or [handler['event_type']]):
      self.handlers[t].discard(handler)

  def handle(self, event):
    for handler in self.handlers[event['type']]:
      handler.handle(event)

Element.register(Score)

