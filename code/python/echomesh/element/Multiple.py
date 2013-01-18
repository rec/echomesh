from __future__ import absolute_import, division, print_function, unicode_literal

from echomesh.util import Log
from echomesh.element import Element

LOGGER = Log.logger(__name__)

class Multiple(Element.Element):
  def __init__(self, parent, element):
    super(Multiple, self, parent, element).__init__()
    self.elements = Element.make(self, element.get('elements', []))
    if not sub_elements_
