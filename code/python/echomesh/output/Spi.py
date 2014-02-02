from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.color import Combine
from echomesh.color import SetupDebianSpiLights
from echomesh.expression import Expression
from echomesh.output.Output import Output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

DEFAULT_SPI_DEVICE = '/dev/spidev0.0'
DEFAULT_GAMMA = 2.5

_LATCH_COUNT = 3

class Spi(Output):
  def RGB(r, g, b):
    return r, g, b

  def GRB(r, g, b):
    return g, r, b

  def BRG(r, g, b):
    return b, r, g

  def __init__(self, count=None, rgb_order='rgb', device=DEFAULT_SPI_DEVICE,
               gamma=DEFAULT_GAMMA, **description):
    assert SetupDebianSpiLights.lights_enabled(), "Lighting is not enabled."
    self.gamma = gamma
    self.rgb_order = getattr(Spi, rgb_order.upper(), None)
    if not self.rgb_order:
      raise Exception('Don\'t understand rgb_order=%s' % rgb_order)

    Config.add_client(self)
    self.count = count
    self.count_set = count is not None
    if self.count_set:
      self._set_lights()
    self._device = open(device, 'wb')
    self.finish_construction(description, is_redirect=False)

  def config_update(self, get):
    if not self.count_set:
      self.count = get('light', 'count')
      self._set_lights()
    self.brightness = Expression.convert(get('light', 'brightness'))

  def _write(self):
    self._device.write(lights)
    self._device.flush()

  def _set_lights(self):
    self.lights = bytearray(0 for i in xrange(3 * self.count + _LATCH_COUNT))
    for i in xrange(_LATCH_COUNT):
      self.lights[-1 - i] = 0

  def emit_output(self, data):
    lights = Combine.combine(data)
    lights.scale(self.brightness)
    lights.gamma(self.gamma)

    for i, light in enumerate(lights):
      light_bytes = self.rgb_order(*light.rgb_range(128, 256))
      self.lights[3 * i: 3 * (i + 1)] = light_bytes

