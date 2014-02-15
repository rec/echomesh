from __future__ import absolute_import, division, print_function, unicode_literals

import six

from echomesh.base import DataFile
from echomesh.element import Element
from echomesh.element.Sequence import Sequence
from echomesh.output.Registry import make_output
from echomesh.pattern.Registry import make_pattern
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class PatternElement(Element.Element):
  def __init__(self, parent, description):
    super(PatternElement, self).__init__(parent, description)

    assert isinstance(parent, Sequence)
    self.pattern = make_pattern(parent, description['pattern'],
                                patterns=parent.patterns)
    self.output_name = description.get('output') or parent.output
    self.output = None

  def class_name(self):
    return 'pattern(%s)' % self.pattern.name

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
    return [self.pattern.evaluate()]
