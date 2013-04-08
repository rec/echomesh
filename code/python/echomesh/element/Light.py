from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.base import Config
from echomesh.color import LightSingleton
from echomesh.element import Renderer
from echomesh.element import Sequence
from echomesh.expression import Units
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Light(Sequence.Sequence):
  def __init__(self, parent, description):
    self.renderers = Renderer.make_renderers(self, description.get('patterns', {}))
    self.device = None
    LightSingleton.add_owner()
    super(Light, self).__init__(parent, description)

  def _on_unload(self):
    super(Light, self)._on_unload()
    LightSingleton.remove_owner()
