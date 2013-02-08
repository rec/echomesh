from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Name
from echomesh.util import Log
from echomesh.element import Element

LOGGER = Log.logger(__name__)

class Handler(Element.Element):
  def __init__(self, parent, description):
    super(Handler, self).__init__(parent, description)
    self.handler_parent = None

  def _on_start(self):
    p = self
    while p and not hasattr(p, 'add_handler'):
      p, childp = p.parent, p
      if childp == p:
        LOGGER.error('Found a recursive handler loop')
        p = None

    if p:
      self.handler_parent = p
      p.add_handler(self)
    else:
      LOGGER.warning("Didn't find a handler parent in open for %s", self)

  def _on_stop(self):
    if hasattr(self.handler_parent, 'remove_handler'):
      self.handler_parent.remove_handler(self)
    else:
      LOGGER.warning("Didn't find a handler parent in close for %s", self)

Element.register(Handler)
