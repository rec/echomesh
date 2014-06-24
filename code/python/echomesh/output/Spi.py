from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.Cechomesh import cechomesh

from echomesh.base import Config
from echomesh.color import SetupDebianSpiLights
from echomesh.color.LightCount import light_count
from echomesh.expression import Expression
from echomesh.output.Poll import Poll
from echomesh.util import Log

LOGGER = Log.logger(__name__)

DEFAULT_SPI_DEVICE = '/dev/spidev0.0'
DEFAULT_GAMMA = 2.5

_LATCH_COUNT = 3

EMULATION_FILE = '/tmp/spi-emulation.txt'

class Spi(Poll):
  def __init__(self, count=None, order='rgb', device=DEFAULT_SPI_DEVICE,
               gamma=DEFAULT_GAMMA, period=None, **description):
    self.enabled = SetupDebianSpiLights.lights_enabled()
    if not self.enabled:
      LOGGER.info('SPI running in emulation mode.')
    self.gamma = gamma
    self.order = cechomesh.get_spi_order(order)
    self.period = period
    self.period_set = period is not None

    self.count_set = count is not None
    if self.count_set:
      self._set_count(count)
    Config.add_client(self)
    if self.enabled:
      self._device = open(device, 'wb')
    super(Spi, self).__init__(
      is_redirect=False, period=self.period, **description)

  def config_update(self, get):
    if not self.count_set:
      self._set_count(light_count(get))
    self.brightness = Expression.convert(get('light', 'brightness'))
    if not self.period_set:
      self.period = Expression.convert(get('light', 'visualizer', 'period'))

  def _write(self):
    if self.enabled:
      self._device.write(self.lights)
      self._device.flush()
    elif self.lights and not getattr(self, 'emulation_written', False):
      self.emulation_written = True
      with open(EMULATION_FILE, 'w') as f:
        f.write(str(list(self.lights)))

  def _set_count(self, count):
    self.count = count
    self.lights = bytearray(0 for i in xrange(3 * count + _LATCH_COUNT))
    for i in xrange(_LATCH_COUNT):
      self.lights[-1 - i] = 0

  def emit_output(self, data):
    if data:
      cechomesh.combine_to_spi(
        data, self.brightness, self.gamma, self.lights, self.order)

      self._write()
