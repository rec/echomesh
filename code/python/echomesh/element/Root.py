from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import time

from echomesh.base import Config
from echomesh.element import Audio, Handler, Image, Mapper, Print, Random
from echomesh.element import Select, Sequence, TextToSpeech, TwitterSearch
from echomesh.element import Element
from echomesh.element import Load

class Root(Element.Element):
  def __init__(self, parent, description, score_file):
    super(Root, self).__init__(parent, description)
    self.score_file = score_file
    self.handlers = {}
    self.elements = Load.make(self, description['elements'])
    self.add_slave(*self.elements)
    self.load_time, self.run_time, self.stop_time = time.time(), 0, 0

  def _on_start(self):
    self.run_time = time.time()

  def _on_stop(self):
    self.stop_time = time.time()

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

Element.register(Root)

