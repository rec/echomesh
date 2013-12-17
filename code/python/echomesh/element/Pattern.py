from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.element import Element
from echomesh.light import LightSingleton
from echomesh.pattern import PatternDesc
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Pattern(Element.Element):
  def __init__(self, parent, description):
    super(Pattern, self).__init__(parent, description)

    assert parent.__class__.__name__ == 'Sequence'
    self.pattern_name = description['pattern']
    self.maker = parent.pattern_makers.get(self.pattern_name) or (
      PatternDesc.make_pattern_from_file(parent, self.pattern_name))
    self.bank = description.get('bank', 'light')
    self.is_light = (self.bank == 'light')

    LightSingleton.add_owner()

  def _on_unload(self):
    super(Pattern, self)._on_unload()
    if self.is_light:
      LightSingleton.remove_owner()

  def class_name(self):
    return 'pattern(%s)' % self.pattern_name

  def _on_run(self):
    super(Pattern, self)._on_run()
    if self.is_light:
      LightSingleton.add_client(self.maker)

  def _on_pause(self):
    super(Pattern, self)._on_pause()
    if self.is_light:
      LightSingleton.remove_client(self.maker)
