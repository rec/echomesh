from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.light import SetupDebianSpiLights
from echomesh.output.Output import Output
from echomesh.util import Log

LOGGER = Log.logger(__name__)

DEFAULT_SPI_DEVICE = '/dev/spidev0.0'

_LATCH_BYTE_COUNT = 3
_LATCH = bytearray(0 for i in xrange(_LATCH_BYTE_COUNT))

_INTERNAL_LATCH_BYTE_COUNT = 0

class Spi(Output):
  def RGB(r, g, b):
    return r, g, b

  def GRB(r, g, b):
    return g, r, b

  def BRG(r, g, b):
    return b, r, g

  def __init__(self, count=None, rgb_order='rgb', device=DEFAULT_SPI_DEVICE,
               **description):
    assert SetupDebianSpiLights.lights_enabled(), "Lighting is not enabled."
    self.rgb_order = getattr(Spi, rgb_order.upper(), None)
    if not self.rgb_order:
      raise Exception('Don\'t understand rgb_order=%s' % rgb_order)

    self.device = device
    self.finish_construction(description, is_redirect=False)

  def emit_output(self, data):
    for o in self.output:
      o.emit_output(data)
