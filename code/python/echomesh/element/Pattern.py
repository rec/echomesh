from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import LightSingleton
from echomesh.element import Element

class Pattern(Element.Element):
  def __init__(self, parent, description):
    super(Pattern, self).__init__(parent, description)
    assert parent.__class__.__name__ == 'Sequence'
    self.pattern_name = description['pattern']
    self.maker = parent.pattern_makers[self.pattern_name]
    self.output = description.get('output', 'light')
    if self.output == 'light':
      LightSingleton.add_owner()

  def _on_unload(self):
    super(Pattern, self)._on_unload()
    if self.output == 'light':
      LightSingleton.remove_owner()
      LightSingleton.remove_client(self.maker)

  def class_name(self):
    return 'pattern(%s)' % self.pattern_name

  def _on_run(self):
    super(Pattern, self)._on_run()
    if self.output == 'light':
      LightSingleton.add_client(self.maker)

  def _on_begin(self):
    super(Pattern, self)._on_begin()
    if not self.is_running and self.output == 'light':
      LightSingleton.remove_client(self.maker)

  def _on_pause(self):
    super(Pattern, self)._on_pause()
