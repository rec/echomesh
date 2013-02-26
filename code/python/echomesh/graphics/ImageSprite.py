from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import time

from echomesh.graphics import Shader
from echomesh.util import Log
from echomesh.util.file import DefaultFile
from echomesh.util.math.Envelope import Envelope
from echomesh.util.math import Units
from echomesh.util.thread.Runnable import Runnable
from echomesh.util import ImportIf

pi3d = ImportIf.imp('pi3d')
from pi3d.util.Loadable import Loadable

LOGGER = Log.logger(__name__)

DEFAULT_Z = 100.0

IMAGE_DIRECTORY = DefaultFile.DefaultFile('asset/image')

CACHE = pi3d.TextureCache()

class DeferredSprite(Loadable):
  def __init__(self, repaint, coords, shader, texture):
    super(DeferredSprite, self).__init__()
    self.repaint = repaint
    self.coords = coords
    self.shader = shader
    self.texture = texture

  def _load_opengl(self):
    x, y, z = self.coords
    self.pi3d_sprite = pi3d.ImageSprite(self.texture,
                                        w=self.texture.ix, h=self.texture.iy,
                                        shader=Shader.shader(self.shader),
                                        x=x, y=y, z=z)

CREATE_TEXTURE = True

class ImageSprite(Runnable):
  CACHE = None

  def __init__(self, file=None, loops=1,
               position=(0, 0), rotation=(0, 0, 0),
               size=1, duration=0, z=DEFAULT_Z,
               shader=None, type='', **kwds):
    super(ImageSprite, self).__init__()
    if kwds:
      s = '' if len(kwds) == 1 else 's'
      LOGGER.error('Unknown keyword%s: %s', s, ', '.join(kwds))

    self.imagename = IMAGE_DIRECTORY.expand(file)

    self._loops = loops
    self._loop_number = 0
    self._position = Envelope(position)
    self._rotation = Envelope(rotation)
    self._size = Envelope(size)
    self._z = Envelope(z)

    self._time = 0
    if duration:
      self._duration = Units.convert(duration)
    else:
      envs = [self._position, self._rotation, self._size, self._z]
      self._duration = max(x.length for x in envs)

    if not self._duration:
      LOGGER.warning('An image sprite had a zero duration.')
    texture = CACHE.create(self.imagename)
    self.deferred_sprite = DeferredSprite(self.repaint, self.coords(0), shader,
                                          texture)

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
        LOGGER.debug('Stopping image sprite')
        self.stop()
        return

    sprite = self.deferred_sprite.pi3d_sprite

    sprite.position(*self.coords(elapsed))
    size = self._size.interpolate(elapsed)
    sprite.scale(size, size, size)
    xrot, yrot, zrot = self._rotation.interpolate(elapsed)
    sprite.rotateToX(xrot)
    sprite.rotateToY(yrot)
    sprite.rotateToZ(zrot)
    sprite.draw()

  def _on_start(self):
    self._add_sprite()

  def _add_sprite(self):
    pi3d.Display.Display.INSTANCE.add_sprites(self.deferred_sprite)


  def _on_stop(self):
    pi3d.Display.Display.INSTANCE.remove_sprites(self.deferred_sprite)


