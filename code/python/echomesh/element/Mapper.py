from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import Name
from echomesh.element import Element
from echomesh.element import Handler
from echomesh.element import Load

class Mapper(Handler.Handler):
  def __init__(self, parent, description):
    super(Mapper, self).__init__(parent, description)
    self.target = description.get('target', Name.NAME)
    self.source = description.get('source')
    self.mapping = description.get('mapping', {})
    handlers = description.get('handlers', [])
    self.handlers = Load.load_elements(self, handlers)

    for key, element in six.iteritems(self.mapping):
      self.mapping[key] = Load.load_one_element(self, element)

  def handle(self, event):
    # TODO: this should go elsewhere.
    # TODO: this needs fixing
    if True or (event.get('source', self.source) == self.source and
        event.get('target', self.target) == self.target):
      key = event.get('key')
      mapper = key and hasattr(key, '__hash__') and self.mapping.get(key)
      if mapper:
        event = mapper.handle(event)

      for handler in self.handlers:
        if not event:
          break
        event = handler.handle(event)
      return event
