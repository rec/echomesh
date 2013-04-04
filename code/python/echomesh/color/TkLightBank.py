from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import threading
import time

from echomesh.base import Config
from echomesh.color.LightBank import LightBank
from echomesh.color import ColorTable
from echomesh.util.thread import MainThreadRunner

DISABLE_EVERYTHING = True

def _get_dimension(count, columns, rows):
  if not (columns or rows):
    columns = 32
  elif not columns:
    columns = 1 + (count - 1) // columns
  if not rows:
    rows = 1 + (count - 1) // columns
  return columns, rows

class TkLightBank(LightBank):
  def _before_thread_start(self):
    super(TkLightBank, self)._before_thread_start()
    Config.add_client(self)
    MainThreadRunner.run_on_main_thread(self.initialize_tk)

  def initialize_tk(self):
    import Tkinter
    self.tkwin = Tkinter.Tk()
    if not DISABLE_EVERYTHING:
      self.tkwin.geometry('%dx%d' % (self.width, self.height))
      self.tkwin.configure(background=self.background)
      self.canvas = Tkinter.Canvas(self.tkwin,
                                   width=self.width, height=self.height)
      self.canvas.pack()
      self.lights = [self._make_light(i) for i in range(self.count)]
    MainThreadRunner.run_every_time(self.tkwin.update)
    self.tkwin.update()

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
    self.width = (self.padding['left'] +
                  self.columns * (self.size[0] + self.padding['light']['x']) +
                  self.padding['right'])
    self.height = (self.padding['top'] +
                   self.rows * (self.size[1] + self.padding['light']['y']) +
                   self.padding['bottom'])

  def _make_light(self, index):
    column = index % self.columns
    row = index // self.columns
    x = (self.padding['left'] +
         column * (self.size[0] + self.padding['light']['x']))

    y = (self.padding['top'] +
         row * (self.size[1] + self.padding['light']['y']))
    if self.shape == 'square':
      method = self.canvas.create_rectangle
    else:
      method = self.canvas.create_oval
    return method(x, y, x + self.size[0], y + self.size[1],
                  outline=self.border_color)

  def clear(self):
    if not DISABLE_EVERYTHING:
      def _clear():
        for light in self.lights:
          self.canvas.itemconfig(light, fill='black')
        self.canvas.pack()
      MainThreadRunner.run_on_main_thread(_clear)

  def _display_lights(self, lights):
    if not DISABLE_EVERYTHING:
      def display():
        for i, color in enumerate(lights):
          self.canvas.itemconfig(self.lights[i], fill=ColorTable.to_tk(color))
        self.canvas.pack()
      MainThreadRunner.run_on_main_thread(display)
