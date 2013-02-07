from __future__ import absolute_import, division, print_function, unicode_literals

import numpy

from echomesh.graphics import GammaTable

# Inspired by:
# https://github.com/adammhaile/RPi-LPD8806/blob/master/LPD8806.py#L90
class LEDBank(object):
  RGB_ORDER = lambda r, g, b: (r, g, b)
  GRB_ORDER = lambda r, g, b: (g, r, b)
  BRG_ORDER = lambda r, g, b: (b, r, g)

  def __init__(self, count, device='/dev/spidev0.0',
               correct = GammaTable.correct,
               channel_order = LEDBank.RGB_ORDER):
    self.count = count
    self.channel_order = channel_order
    self.correct = correct
    self.buffer = bytearray(3 * count + 4)
    self.buffer_dirty = False
    self.pixels = numpy.array([0.0] * (3 * count))
    self.pixels_dirty = False
    self.device = device
    self.spi = open(device, 'wb')
    self.brightness = 1.0

  def set_brightness(self, brightness):
    self.brightness = brightness
    self.pixels_dirty = True

  def update(self):
    if self.pixels_dirty:
      for i in range(self.count):
        self._set_buffer_entry(i)
      self.buffer_dirty = True
      self.pixels_dirty = False

    if self.buffer_dirty:
      self.spi.write(self.buffer)
      self.buffer_dirty = False

  def set_pixel(self, i, rgb):
    self.pixels[3 * i:3 * (i + 1)] = rgb
    self._set_buffer_entry(i)
    self.buffer_dirty = True

  def _set_buffer_entry(self, i):
    b, e = 3 * i, 3 * (i + 1)
    rgb = (self.correct(self.pixels[i] * self.brightness) for i in range(b, e))
    self.buffer[b:e] = self.channel_order(*rgb)

