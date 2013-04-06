from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import threading
import time

from six.moves import xrange

from echomesh.base import Config
from echomesh.color.LightBank import LightBank
from echomesh.color import ColorTable
from echomesh.util.thread import TkThreadRunner

BLACK = '#000000'

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
    self.tk_count = 0
    self.light_count = 0
    super(TkLightBank, self)._before_thread_start()
    Config.add_client(self)
    TkThreadRunner.run_on_main_thread(self.initialize_tk)

  def _after_thread_pause(self):
    super(TkLightBank, self)._after_thread_pause()
    Config.remove_client(self)
    TkThreadRunner.run_on_main_thread(self.tkwin.destroy)

  def initialize_tk(self):
    import Tkinter
    self.tkwin = Tkinter.Tk()
    self.tkwin.geometry('%dx%d' % (self.width, self.height))
    self.tkwin.configure(background=self.background)
    self.canvas = Tkinter.Canvas(self.tkwin,
                                 width=self.width, height=self.height)
    self.canvas.pack()
    self.lights = [self._make_light(i) for i in xrange(self.count)]
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
    def _clear():
      for i in xrange(self.count):
        self.canvas.itemconfig(self.lights[i], fill=BLACK)
      self.tkwin.update()
    TkThreadRunner.run_on_main_thread(_clear)

  def _display_lights(self, lights):
    def display():
      for i in xrange(self.count):
        color = ColorTable.to_tk(lights[i]) if i < len(lights) else BLACK
        self.canvas.itemconfig(self.lights[i], fill=color)
      self.tkwin.update()
      self.tk_count += 1

    TkThreadRunner.run_on_main_thread(display)
    self.light_count += 1
