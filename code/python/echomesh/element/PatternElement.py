from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import DataFile
from echomesh.element import Element
from echomesh.element.Sequence import Sequence
from echomesh.output import make_output
from echomesh.pattern import PatternDesc
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class PatternElement(Element.Element):
  def __init__(self, parent, description):
    super(PatternElement, self).__init__(parent, description)

    assert isinstance(parent, Sequence)
    self.pattern_name = description['pattern']
    self.maker = parent.pattern_makers.get(self.pattern_name) or (
      PatternDesc.make_pattern_from_file(parent, self.pattern_name))
    self.output_name = description.get('output') or parent.output
    self.output = None

  def class_name(self):
    return 'pattern(%s)' % self.pattern_name

  def _on_run(self):
    super(PatternElement, self)._on_run()
    if not self.output:
      self.output = make_output(self.output_name)
      self.output.add_client(self)

  def _on_unload(self):
    if self.output:
      self.output.remove_client(self)
      self.output = None

  def evaluate(self):
    return [self.maker.evaluate()]