from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import threading
import time

from six.moves import xrange

from echomesh.base import Config
from echomesh.color.LightBank import LightBank
from echomesh.color import ColorTable
from echomesh.expression import UnitConfig
from echomesh.util import Log
from echomesh.util.thread import TkThreadRunner

LOGGER = Log.logger(__name__)
BLACK = '#000000'
WINDOW_TITLE = 'Lighting visualization window.'

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
    self.count_difference = 1
    self.lock = threading.Lock()
    self.last_get = {}
    self.tkwin = None
    self.count = 0
    self.lights = []

    super(TkLightBank, self)._before_thread_start()
    TkThreadRunner.run()
    Config.add_client(self)

  def destroy(self):
    TkThreadRunner.stop()
    self.tkwin.destroy()
    self.tkwin = None

  def _after_thread_pause(self):
    super(TkLightBank, self)._after_thread_pause()
    def destroy():
      TkThreadRunner.stop()
      with self.lock:
        tkwin, self.tkwin = self.tkwin, None
        tkwin.destroy()
    TkThreadRunner.defer(destroy)

  def initialize_tk(self):
    with self.lock:
      if self.tkwin:
        import Tkinter
        self.canvas.delete(Tkinter.ALL)
      else:
        import Tkinter
        self.tkwin = Tkinter.Tk()
        self.tkwin.title(WINDOW_TITLE)
        self.canvas = Tkinter.Canvas(self.tkwin,
                                     width=self.width, height=self.height)
      if 'rectangle'.startswith(self.shape):
        self.method = self.canvas.create_rectangle
      else:
        self.method = self.canvas.create_oval
      self.tkwin.geometry('%dx%d' % (self.width, self.height))
      self.tkwin.configure(background=self.background)
      self.canvas.pack()
      self.lights = [self._make_light(i) for i in xrange(self.count)]
      self.tkwin.update()

  def config_update(self, get):
    count = Config.get('light', 'count')
    def _get(*items):
      return get(*(('light', 'display') + items))

    last_get = _get()
    if self.last_get == last_get and self.count == countn:
      return
    self.last_get = copy.deepcopy(last_get)
    self.count = count

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
    TkThreadRunner.defer(self.initialize_tk)

  def _make_light(self, index):
    column = index % self.columns
    row = index // self.columns
    x = (self.padding['left'] +
         column * (self.size[0] + self.padding['light']['x']))

    y = (self.padding['top'] +
         row * (self.size[1] + self.padding['light']['y']))
    return self.method(x, y, x + self.size[0], y + self.size[1],
                       outline=self.border_color)

  def clear(self):
    def _clear():
      with self.lock:
        if self.tkwin:
          for i in xrange(self.count):
            self.canvas.itemconfig(self.lights[i], fill=BLACK)
          self.tkwin.update()
    TkThreadRunner.defer(_clear)

  def _display_lights(self, lights):
    brightness = UnitConfig.get('light', 'brightness')
    light_colors = [ColorTable.to_tk(light, brightness) for light in lights]
    diff = self.count - len(lights)
    if diff > 0:
      light_colors += [BLACK] * diff

    def display():
      with self.lock:
        if self.tkwin:
          for i in xrange(self.count):
            self.canvas.itemconfig(self.lights[i], fill=light_colors[i])
          self.tkwin.update()
          self.tk_count += 1

    TkThreadRunner.defer(display)
    self.light_count += 1

    count_difference = self.light_count - self.tk_count
    if count_difference > self.count_difference:
      if count_difference > 10 and count_difference < 50:
        LOGGER.error('Tk is behind by %s frames - reduce config.light.period',
                     count_difference)
      self.count_difference = count_difference
