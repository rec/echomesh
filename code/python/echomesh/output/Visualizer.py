from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.color import Combiner
from echomesh.expression import Expression
from echomesh.output.Poll import Poll
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class Visualizer(Poll):
  def __init__(self, light_count=None, interval=None, **kwds):
    assert cechomesh.is_started()
    self.lighting_window = cechomesh.PyLightingWindow()
    self.interval = interval
    self.interval_set = interval is not None
    self.light_count_set = light_count is not None
    if self.light_count_set:
      self.set_light_count(light_count)

    Config.add_client(self)
    super(Visualizer, self).__init__(
      is_redirect=False, interval=self.interval, **kwds)

  def _after_thread_pause(self):
    self.lighting_window.close()

  def snapshot(self, filename):
    self.lighting_window.save_snapshot_to_file(filename)

  def config_update(self, get):
    if not self.light_count_set:
      self.set_light_count(get('light', 'count'))
    if not self.interval_set:
      self.interval = Expression.convert(get('light', 'visualizer', 'period'))

  def set_light_count(self, light_count):
    self.lighting_window.set_light_count(light_count)

  def emit_output(self, data):
    if data:
      self.lighting_window.set_clights(Combiner.ccombine(data))
