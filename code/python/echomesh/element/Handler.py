from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.base import Name
from echomesh.util import Log
from echomesh.element import Element
from echomesh.element import Load
from echomesh.element import Register

LOGGER = Log.logger(__name__)

class Handler(Element.Element):
  def __init__(self, parent, description):
    super(Handler, self).__init__(parent, description)
    self.target = description.get('target', Name.NAME)
    self.source = description.get('source', None)
    self.mapping = description.get('mapping', {})
    self.read_repeated('handlers')

    for k, v in self.mapping.iteritems():
      self.mapping[k] = Load.make(self, v)[0]

  def handle(self, event):
    if (event.get('source', self.source) == self.source and
        event.get('target', self.target) == self.target):
      key = event.get('key', None)
      mapper = key and hasattr(key, '__hash__') and self.mapping.get(key, None)
      if mapper:
        event = mapper(event)

      for handler in self.handlers:
        if not event:
          break
        event = handler.handle(event)
      return event

Register.register(Handler)
