from __future__ import absolute_import, division, print_function, unicode_literals

import threading

from echomesh.base import Config
from echomesh.color import Combiner
from echomesh.color import LightSingleton
from echomesh.element import Element
from echomesh.element import Scene
from echomesh.element import Sequence
from echomesh.expression import Units
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Light(Sequence.Sequence):
  def __init__(self, parent, description):
    scenes = description.get('scenes', {}).iteritems()
    self.scenes = dict((k, Scene.scene(self, v)) for k, v in scenes)
    self.timeout = Units.convert(description.get('period', '50ms'))
    self.active_scenes = set()
    self.device = None
    self.light_count = Config.get('light', 'count')
    self.lock = threading.Lock()
    super(Light, self).__init__(parent, description)
