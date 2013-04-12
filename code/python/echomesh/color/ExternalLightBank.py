from __future__ import absolute_import, division, print_function, unicode_literals

import subprocess


from echomesh.base import Platform
from echomesh.util import Log

LOGGER = Log.logger(__name__)

class ExternalLightBank(object):
  def __init__(self, count=None):
    super(ExternalLightBank, self).__init__(count=count)

  def clear(self):
    with self.lock:
      self._write(self._clear)

  def _before_thread_start(self):
    super(ExternalLightBank, self)._before_thread_start()
    self._device = open('/dev/spidev0.0', 'wb')

  def _after_thread_pause(self):
    super(ExternalLightBank, self)._after_thread_pause()
    self._device.close()
    self._device = None

  def _display_lights(self, lights):
    brightness = UnitConfig.get('light', 'brightness')

    for i, light in enumerate(lights):
      if light is None:
        light = [0x80, 0x80, 0x80]
      else:
        light =  self.order(*int(min(0x80 + 0x7F * x * brightness, 0xFF)
                                 for x in light)
      self._bank[3 * i:3 * (i + 1)] = light
    self._write(self.pattern)


