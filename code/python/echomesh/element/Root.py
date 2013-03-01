from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import datetime
import time

from echomesh.base import Config
from echomesh.element import Audio, Handler, Image, List, Mapper, Print, Repeat
from echomesh.element import Select, Sequence, TextToSpeech, TwitterSearch
from echomesh.element import Element
from echomesh.element import Load

PRINT_FORMAT = '{state:4} {class:10} {time:9}'

class Root(List.List):
  def __init__(self, description, score):
    super(Root, self).__init__(None, description)
    self.score = score
    self.handlers = {}

  def add_handler(self, handler, *types):
    if not types:
      types = handler.event_type
      if not types:
        raise Exception('Handler needs to have an event_type')
      types = [types]
    for t in (types or []):
      self.handlers.setdefault(t, set()).add(handler)

  def __str__(self):
    return PRINT_FORMAT.format(**self.element[0].info())

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


def _format_delta(t):
  s = str(datetime.timedelta(seconds=t))
  loc = s.find('.')
  if loc > 0:
    s = s[0:loc]
  return s


Element.register(Root)
