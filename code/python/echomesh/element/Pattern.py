from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import LightSingleton
from echomesh.element import Element

class Pattern(Element.Element):
  def __init__(self, parent, description):
    super(Pattern, self).__init__(parent, description)
    assert parent.__class__.__name__ == 'Light'
    self.renderer = parent.renderers[description['pattern']]

  def _on_run(self):
    super(Pattern, self)._on_run()
    LightSingleton.add_client(self.renderer)

  def _on_pause(self):
    super(Pattern, self)._on_pause()
    LightSingleton.remove_client(self.renderer)
