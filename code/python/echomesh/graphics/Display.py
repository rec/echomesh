from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.base import Config
from echomesh.graphics import Shader
from echomesh.util import ImportIf
from echomesh.util import Log
from echomesh.util.thread import MainThreadRunner
from echomesh.util.thread import Runnable

pi3d = ImportIf.imp('pi3d')

LOGGER = Log.logger(__name__)

DEFAULT_TIMEOUT = 0.2

class Display(Runnable.Runnable):
  def __init__(self):
    super(Display, self).__init__()
    self.timeout = DEFAULT_TIMEOUT
    if not Config.get('load_module', 'pi3d'):
      self.display = None
      return

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

    self.display = pi3d.Display.create(**keywords)
    Config.add_client(self)
    Shader.SHADER()  # Make sure that the shader is created in the main thread!

  def config_update(self, get):
    if self.display:
      self.display.frames_per_second = get('pi3d', 'frames_per_second')

  def _on_run(self):
    super(Display, self)._on_run()
    if self.display:
      self.display.first_time = True
      self.display.is_running = True

  def _on_pause(self):
    super(Display, self)._on_pause()
    if self.display:
      self.display.stop()

  def loop(self):
    while self.is_running:
      if self.display:
        if self.display.loop_running():
          MainThreadRunner.run_one()
        else:
          self.pause()
      else:
        MainThreadRunner.run_one(self.timeout)
