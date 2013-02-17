from __future__ import absolute_import, division, print_function, unicode_literals

import collections

from echomesh.base import Config
from echomesh.element import Element
from echomesh.element import Load

class Score(Element.Element):
  def __init__(self, parent, description):
    self.handlers = {}

    super(Score, self).__init__(parent, description)
    self.elements = Load.make(self, description['elements'])
    self.add_slave(*self.elements)
    self.name = ''

  def add_handler(self, handler, *types):
    if not types:
      types = handler.event_type
      if not types:
        raise Exception('Handler needs to have an event_type')
      types = [types]
    for t in (types or []):
      self.handlers.setdefault(t, set()).add(handler)

  def remove_handler(self, handler, *types):
    for t in (types or [handler['event_type']]):
      self.handlers.get(t, set()).discard(handler)

  def handle(self, event):
    if self.handlers:
      event_type = event.get('event_type')
      if not event_type:
        raise Exception('The event %s had no type' % event)
      handlers = self.handlers.get(event_type) or []
      for handler in handlers:
        handler.handle(event)

Element.register(Score)
