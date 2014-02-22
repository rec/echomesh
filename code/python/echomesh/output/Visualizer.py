from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.color import Combine
from echomesh.expression import Expression
from echomesh.output.Poll import Poll
from echomesh.util.config.ConfigValues import ConfigValues
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Visualizer(Poll):
  INSTANCE = None

  def __init__(self, **values):
    if not Visualizer.INSTANCE:
      Visualizer.INSTANCE = self

    self.values = ConfigValues(
      configs={
        'light_count': 'light.count',
        'period': 'light.visualizer.period',
        'transform': 'light.visualizer.transform',
        'brightness': 'light.brightness',
        },
      values=values,
      update_callback=self.update_callback)

    assert cechomesh.is_started()
    self.lighting_window = cechomesh.PyLightingWindow()
    super(Visualizer, self).__init__(is_redirect=False)
    self.values.add_client()

  def _after_thread_pause(self):
    self.lighting_window.close()

  def snapshot(self, filename):
    self.lighting_window.save_snapshot_to_file(filename)

  def update_callback(self):
    self.period = Expression.convert(self.values.period)
    self.set_light_count(self.values.light_count)
    self.transform = self.values.transform
    if self.transform:
      try:
        self.transform = cechomesh.Transform(self.transform)
      except:
        LOGGER.error('Don\'t understand transform %s', self.transform)
        self.transform = None
    self.brightness = Expression.convert(self.values.brightness)
    if self.transform:
      self.brightness = self.transform.apply(self.brightness)

  def set_light_count(self, light_count):
    self.lighting_window.set_light_count(light_count)

  def emit_output(self, data):
    lights = Combine.combine(data)
    lights.scale(self.brightness)
    self.lighting_window.set_lights(lights)
