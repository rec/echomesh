from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.color import Combiner
from echomesh.light.LightBank import LightBank
from echomesh.util import Log

class SpiLightBank(LightBank):
  def _make_data(self, count):
    return bytearray(3 * self.count)

  def _fill_data(self, client_lights, brightness):
    Combiner.combine_to_bytearray(self.data, client_lights, brightness)

