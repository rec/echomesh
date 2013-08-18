from __future__ import absolute_import, division, print_function, unicode_literals

import time

from pi3d import Display

from echomesh.base import Config
from echomesh.expression import Expression
from echomesh.graphics import Shader
from echomesh.util import ImportIf
from echomesh.util.thread import Runnable

class Pi3dDisplay(Runnable.Runnable):
  def __init__(self):
    super(Pi3dDisplay, self).__init__()
    self.timeout = Expression.convert(Config.get('network', 'timeout'))
    keywords = {}

    background = Config.get('pi3d', 'background')
    if background:
      keywords.update(background=background)

    dimensions = Config.get('pi3d', 'dimensions')
    if dimensions:
      x, y, width, height = dimensions
      keywords.update(x=x, y=y, width=width, height=height)

    for k in ['aspect', 'depth', 'far', 'near', 'tk', 'window_title']:
      keywords[k] = Config.get('pi3d', k)

    self.display = Display.create(**keywords)
    Config.add_client(self)
    Shader.SHADER()  # Make sure that the shader is created in the main thread!

  def config_update(self, get):
    if self.display:
      self.display.frames_per_second = get('pi3d', 'frames_per_second')

  def _on_run(self):
    super(Pi3dDisplay, self)._on_run()
    self.display.first_time = True
    self.display.is_running = True

  def _on_pause(self):
    super(Pi3dDisplay, self)._on_pause()
    self.display.stop()

  def loop(self):
    while self.is_running:
      if not self.display.loop_running():
        self.pause()
