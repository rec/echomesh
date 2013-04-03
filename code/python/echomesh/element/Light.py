from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.base import Config
from echomesh.element import Renderer
from echomesh.element import Sequence
from echomesh.expression import Units
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Light(Sequence.Sequence):
  def __init__(self, parent, description):
    self.renderers = Renderer.make_renderers(self, description.get('scenes', {}))
    self.device = None
    self.light_count = Config.get('light', 'count')
    self.lock = threading.Lock()
    super(Light, self).__init__(parent, description)
