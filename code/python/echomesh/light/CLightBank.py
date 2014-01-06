from __future__ import absolute_import, division, print_function, unicode_literals

import base64
import copy
import cechomesh

from echomesh.light.SpiLightBank import SpiLightBank
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class CLightBank(SpiLightBank):
  def __init__(self):
    super(CLightBank, self).__init__(is_daemon=True)
    assert cechomesh.is_started()
    self.lighting_window = cechomesh.PyLightingWindow()

  def snapshot(self, filename):
    self.lighting_window.save_snapshot_to_file(filename)

  def _on_pause(self):
    self.lighting_window.close()

  def _display_lights(self):
    self.lighting_window.set_lights(self.data)

  def _make_data(self, count):
    self.lighting_window.set_light_count(count)
    return super(CLightBank, self)._make_data(count)

