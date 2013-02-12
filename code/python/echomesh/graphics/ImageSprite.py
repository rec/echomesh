from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import time

from echomesh.graphics import Shader
from echomesh.util import Log
from echomesh.util.file import DefaultFile
from echomesh.util.math.Envelope import Envelope
from echomesh.util.thread.Runnable import Runnable
from echomesh.util import ImportIf

pi3d = ImportIf.imp('pi3d')

LOGGER = Log.logger(__name__)

DEFAULT_Z = -2.0

IMAGE_DIRECTORY = DefaultFile.DefaultFile('asset/image')

class ImageSprite(Runnable):
  CACHE = None

  def __init__(self, file=None, loops=1,
               position=(0, 0), rotation=0, size=1, duration=0, z=DEFAULT_Z,
               shader=None, **kwds):
    super(ImageSprite, self).__init__()
    self._imagename = IMAGE_DIRECTORY.expand(file)
    LOGGER.debug('Opening sprite %s', self._imagename)

    self._loops = loops
    self._loop_number = 0
    self._position = Envelope(position)
    self._rotation = Envelope(rotation)
    self._size = Envelope(size)
    self._z = Envelope(z)

    x, y, z = self.coords(0)
    if not ImageSprite.CACHE:
      ImageSprite.CACHE = pi3d.TextureCache()
    texture = ImageSprite.CACHE.create(self._imagename, defer=True)
    self.pi3d_sprite = pi3d.ImageSprite(texture,
                                        w=texture.ix, h=texture.iy,
                                        shader=Shader.shader(shader),
                                        x=x, y=y, z=z)
    setattr(self.pi3d_sprite, 'repaint', self.repaint)

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

    self.pi3d_sprite.position(*self.coords(elapsed))
    size = self._size.interpolate(elapsed)
    self.pi3d_sprite.scale(size, size, size)
    self.pi3d_sprite.rotateToZ(self._rotation.interpolate(elapsed))

    self.pi3d_sprite.draw()

  def _on_start(self):
    pi3d.Display.Display.INSTANCE.add_sprites(self.pi3d_sprite)

  def _on_stop(self):
    pi3d.Display.Display.INSTANCE.remove_sprites(self.pi3d_sprite)

