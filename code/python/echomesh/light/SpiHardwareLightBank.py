from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.light import SetupDebianSpiLights
from echomesh.light.SpiLightBank import SpiLightBank
from echomesh.util import Log

LOGGER = Log.logger(__name__)

SPI_DEVICE = '/dev/spidev0.0'

_LATCH_BYTE_COUNT = 3
_LATCH = bytearray(0 for i in xrange(_LATCH_BYTE_COUNT))

_INTERNAL_LATCH_BYTE_COUNT = 0

class SpiHardwareLightBank(SpiLightBank):
  def RGB(r, g, b):
    return r, g, b

  def GRB(r, g, b):
    return g, r, b

  def BRG(r, g, b):
    return b, r, g

  def __init__(self, count=None):
    assert SetupDebianSpiLights.lights_enabled(), "Lighting is not enabled."

    super(SpiHardwareLightBank, self).__init__(count=count)
    order = Config.get('light', 'hardware', 'rgb_order')
    self.order = getattr(SpiHardwareLightBank, order.upper(), None)
    if not self.order:
      LOGGER.error("Didn't understand order %s", order)
    self._clear, self._bank = self._light_array(), self._light_array()

  def _light_array(self):
    count = Config.get('light', 'count')
    b = bytearray(0 for i in xrange(count + _INTERNAL_LATCH_BYTE_COUNT))
    if False:  # TODO
      for i in xrange(_INTERNAL_LATCH_BYTE_COUNT):
        b[-1 - i] = 0
    return b

  def _write(self, lights):
    self._device.write(lights)
    self._device.flush()
    if _LATCH_BYTE_COUNT:
      self._device.write(_LATCH)
      self._device.flush()

  def clear(self):
    with self.lock:
      self._write(self._clear)

  def _before_thread_start(self):
    super(SpiHardwareLightBank, self)._before_thread_start()
    self._device = open(SPI_DEVICE, 'wb')

  def _after_thread_pause(self):
    super(SpiHardwareLightBank, self)._after_thread_pause()
    self._device.close()
    self._device = None

  def _display_lights(self, lights, brightness):
    for i, light in enumerate(lights):
      if light is None:
        light = [0x80, 0x80, 0x80]
      else:
        light =  self.order(*int(min(0x80 + 0x7F * x * brightness, 0xFF)
                                 for x in light))
      self._bank[3 * i:3 * (i + 1)] = light
    self._write(self.pattern)
