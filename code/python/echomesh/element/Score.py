from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.element import Load

class Score(Element.Element):
  def __init__(self, parent, description):
    super(List, self).__init__(parent, description)
    self.elements = Load.make(description)
    self.add_slave(*self.elements)

def make_score(parent, scorefile):
  description = Load.load(scorefile)
  if not description:
    raise Exception('Unable to open score file %s' % scorefile)
  return Score(parent, description)
