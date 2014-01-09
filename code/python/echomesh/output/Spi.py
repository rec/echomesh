from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.color import Combiner
from echomesh.light import SetupDebianSpiLights
from echomesh.output.Output import Output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

DEFAULT_SPI_DEVICE = '/dev/spidev0.0'
DEFAULT_GAMMA = 2.5

_LATCH_BYTE_COUNT = 3
_LATCH = bytearray(0 for i in xrange(_LATCH_BYTE_COUNT))

_INTERNAL_LATCH_BYTE_COUNT = 3

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
    self.rgb_order = getattr(Spi, rgb_order.upper(), None)
    self.gamma = gamma
    if not self.rgb_order:
      raise Exception('Don\'t understand rgb_order=%s' % rgb_order)

    self.count = count or Config.get('light', 'count')
    self._device = open(device, 'wb')
    self.finish_construction(description, is_redirect=False)

  def _write(self, lights):
    self._device.write(lights)
    self._device.flush()
    if _LATCH_BYTE_COUNT:
      self._device.write(_LATCH)
      self._device.flush()

  def _light_array(self):
    return bytearray(0 for i in xrange(self.count + _INTERNAL_LATCH_BYTE_COUNT))
    for i in xrange(_INTERNAL_LATCH_BYTE_COUNT):
      b[-1 - i] = 0
    return b

  def emit_output(self, data):
    lights = Combiner.ccombine(data)
    lights.gamma(self.gamma)
    for l in lights:

