from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import copy
import cechomesh

from echomesh.base import Quit
from echomesh.expression import Expression
from echomesh.light.SpiLightBank import SpiLightBank
from echomesh.output.Poll import Poll
from echomesh.util import Log
from echomesh.util import Log
from echomesh.util.string import Split
from echomesh.base import Config

LOGGER = Log.logger(__name__)

class Visualizer(Poll):
  def __init__(self, light_count=None, *args, **kwds):
    super(self, Poll).__init__(*args, **kwds)
    self.lighting_window = cechomesh.PyLightingWindow()
    if light_count is None:
      Config.add_client(self)
    else:
      self.set_light_count(light_count)

  def snapshot(self, filename):
    self.lighting_window.save_snapshot_to_file(filename)

  def config_update(self, get):
    set_light_count(get('light', 'count'))

  def set_light_count(light_count):
    self.lighting_window.set_light_count(light_count)

  def _on_pause(self):
    self.lighting_window.close()

  def emit_output(self, data):
    self.lighting_window.set_clights(data)

