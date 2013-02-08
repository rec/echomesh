from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import time

from echomesh.graphics import Shader
from echomesh.util import Log
from echomesh.util.math.Envelope import Envelope
from echomesh.util.thread.Runnable import Runnable
from pi3d import Display
from pi3d import Texture
from pi3d.shape import Sprite

LOGGER = Log.logger(__name__)

DEFAULT_Z = -2.0

class ImageSprite(Sprite.ImageSprite, Runnable):
  CACHE = Texture.Cache()

  def __init__(self, file=None, loops=1,
               position=(0, 0), rotation=0, size=1, duration=0, z=DEFAULT_Z,
               shader=None, **kwds):
    Runnable.__init__(self)
    self._imagename = file
    LOGGER.debug('Opening sprite %s', self._imagename)

    self._loops = loops
    self._loop_number = 0
    self._position = Envelope(position)
    self._rotation = Envelope(rotation)
    self._size = Envelope(size)
    self._z = Envelope(z)

    x, y, z = self.coords(0)
    texture = ImageSprite.CACHE.create(file, defer=True)
    Sprite.ImageSprite.__init__(self, texture, shader=Shader.shader(shader),
                                x=x, y=y, z=z)

    self._time = 0
    if duration:
      self._duration = duration
    else:
      envs = [self._position, self._rotation, self._size]
      self._duration = max(x.length for x in envs)

  def coords(self, t):
    x, y = self._position.interpolate(t)
    z = self._z.interpolate(t)
    return x, y, z

  def repaint(self, t):
    if not hasattr(self, 'image'):
      if self._imagename and PI3D_DISPLAY:
        self._image = PI3D_DISPLAY.load_texture(self._imagename)
      else:
        self._image = None
        LOGGER.error('No image in image arguments')

    if not self._time:
      self._time = t
    elapsed = t - self._time
    if elapsed > self._duration:
      self._loop_number += 1
      if self._loop_number < self._loops:
        self._time = 0
        elapsed = 0
      else:
        self.stop()
        return

    self.position(*self.coords(elapsed))
    size = self._size.interpolate(elapsed)
    self.scale(size, size, size)
    self.rotateToZ(self._rotation.interpolate(elapsed))

    self.draw()

  def _on_start(self):
    Display.INSTANCE.add_sprites(self)

  def _on_stop(self):
    Display.INSTANCE.remove_sprites(self)

