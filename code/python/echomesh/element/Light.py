from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.color import Light
from echomesh.element import Element
from echomesh.element import Scene
from echomesh.element import Sequence
from echomesh.expression import Units
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Light(Sequence.Sequence):
  def __init__(self, parent, description):
    super(Light, self).__init__(parent, description)
    scenes = description.get('scenes', {}).iteritems()
    self.scenes = dict((k, Scene.scene(self, v)) for k, v in scenes)
    self.timeout = Units.convert(description.get('period', '50ms'))
    self.active_scenes = set()

  def run_scene(self, scene):
    self.active_scenes.add(self.scenes[scene.scene])

  def pause_scene(self, scene):
    self.active_scenes.remove(self.scenes[scene.scene])

  def single_loop(self):
    super(Light, self).single_loop()
    scenes = [s() for s in self.active_scenes]
    lights = Light.combine(Light.sup, *scenes)
    print(lights)

Element.register(Light)

