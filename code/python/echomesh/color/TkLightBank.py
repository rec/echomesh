from __future__ import absolute_import, division, print_function, unicode_literals

import Tkinter

import copy
import threading
import time

from echomesh.base import Config
from echomesh.color.LightBank import LightBank
from echomesh.color import ColorTable

def _get_dimension(count, columns, rows):
  if not (columns or rows):
    columns = 32
  elif not columns:
    columns = 1 + (count - 1) / columns
  if not rows:
    rows = 1 + (count - 1) / columns
  return columns, rows

class TkLightBank(LightBank):
  def _before_thread_start(self):
    super(TkLightBank, self)._before_thread_start()
    Config.add_client(self)
    self.tkwin = Tkinter.Tk()
    self.tkwin.geometry('%dx%d' % (self.width, self.height))
    self.tkwin.configure(background = self.background)
    self.lights = [self._make_light(i) for i in range(self.count)]

  def config_update(self, get):
    def _get(*items):
      return get(*(('light', 'display') + items))

    def _color(*items):
      return ColorTable.to_tk(ColorTable.to_color(_get(*items)))

    self.border_color = _color('light', 'border', 'color')
    self.button_background = _color('light', 'background')
    self.background = _color('background')
    self.border_width = _get('light', 'border', 'width')
    self.shape = _get('light', 'shape')
    self.size = _get('light', 'size')
    self.padding = _get('padding')
    self.columns, self.rows = _get_dimension(self.count, *_get('layout'))
    self.width = 2 * self.padding + self.columns * (self.size[0] + self.padding)
    self.height = 2 * self.padding + self.rows * (self.size[1] + self.padding)

  def _make_light(self, index):
    column = index % self.columns
    row = index // self.columns
    x = self.padding + (self.size[0] + self.padding) * column
    y = self.padding + (self.size[1] + self.padding) * row
    if self.shape == 'square':
      method = self.tkwin.create_rectangle
    else:
      method = self.tkwin.create_oval
    return method(x, y, x + self.size[0], y + self.size[1],
                  outline=ColorTable.to_tk(*self.border_color),
                  width=self.width, background=self.button_background)

  def _after_thread_pause(self):
    Config.remove_client(self)
    super(TkLightBank, self)._after_thread_pause()
    self._device.close()
    self._device = None

  def clear(self):
    for light in self.lights:
      light.configure(fill='black')

  def _display_lights(self, lights):
    for i, color in enumerate(lights):
      self.lights[i].configure(fill=ColorTable.to_tk(color))
