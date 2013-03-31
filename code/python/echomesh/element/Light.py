from __future__ import absolute_import, division, print_function, unicode_literals

import echomesh.color.Light

from echomesh.base import Config
from echomesh.element import Element
from echomesh.element import Scene
from echomesh.element import Sequence
from echomesh.expression import Units
from echomesh.util import Log

LOGGER = Log.logger(__name__)

LATCH_BYTE_COUNT = 3

def _light_array(count, x=0x80):
  b = bytearray(x for i in xrange(count))
  for i in range(LATCH_BYTE_COUNT):
    b[-1 - i] = 0
  return b

class Light(Sequence.Sequence):
  def __init__(self, parent, description):
    super(Light, self).__init__(parent, description)
    scenes = description.get('scenes', {}).iteritems()
    self.scenes = dict((k, Scene.scene(self, v)) for k, v in scenes)
    self.timeout = Units.convert(description.get('period', '50ms'))
    self.active_scenes = set()
    self.device = None
    self.light_count = Config.get('light', 'count')
    self.clear = _light_array(self.light_count)
    self.pattern = _light_array(self.light_count)

  def _write(self, lights):
    self.device.write(lights)

  def _clear(self):
    self._write(self.clear)

  def _on_run(self):
    super(Light, self)._on_run()
    self.device = open('/dev/spidev0.0', 'wb')
    self._clear()

  def _on_pause(self):
    self._clear()
    self.device.close()
    self.device = None

  def run_scene(self, scene):
    self.active_scenes.add(self.scenes[scene.scene])

  def pause_scene(self, scene):
    self.active_scenes.remove(self.scenes[scene.scene])

  def single_loop(self):
    super(Light, self).single_loop()
    scenes = [s() for s in self.active_scenes]
    lights = echomesh.color.Light.combine(max, *scenes)
    for i, light in enumerate(lights):
      if light is None:
        light = (0, 0, 0)
      self.pattern[3 * i:3 * i + 3] = light
    self._write(self.pattern)

Element.register(Light)
