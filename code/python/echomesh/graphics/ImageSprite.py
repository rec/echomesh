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

CREATE_SPRITE_IN_CONSTRUCTOR = not True

class DeferredSprite(Loadable):
  def __init__(self, repaint, imagename, coords):
    super(DeferredSprite, self).__init__()
    self.repaint = repaint
    self.imagename = imagename
    self.coords = coords

  def _load_opengl(self):
    if not ImageSprite.CACHE:
      ImageSprite.CACHE = pi3d.TextureCache()
    texture = ImageSprite.CACHE.create(self.imagename, defer=False)
    x, y, z = self.coords
    self.pi3d_sprite = pi3d.ImageSprite(texture,
                                        w=texture.ix, h=texture.iy,
                                        shader=Shader.DEFAULT_SHADER,
                                        # shader=Shader.shader(shader),
                                        x=x, y=y, z=z)

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
    LOGGER.debug('Opening sprite %s', self.imagename)

    self._loops = loops
    self._loop_number = 0
    self._position = Envelope(position)
    self._rotation = Envelope(rotation)
    self._size = Envelope(size)
    self._z = Envelope(z)

    assert not shader, "We can't create shaders except on the main thread."
    self._time = 0
    if duration:
      self._duration = Units.convert(duration)
    else:
      envs = [self._position, self._rotation, self._size, self._z]
      self._duration = max(x.length for x in envs)

    if not self._duration:
      LOGGER.warning('An image sprite had a zero duration.')
    self._sprite = None
    self.sprite_added = False
    if CREATE_SPRITE_IN_CONSTRUCTOR:
      self.sprite()
    else:
      self.deferred_sprite = DeferredSprite(self.repaint, self.imagename,
                                            self.coords(0))

  def sprite(self):
    if not self._sprite:
      print('CREATING sprite')
      x, y, z = self.coords(0)
      if not ImageSprite.CACHE:
        ImageSprite.CACHE = pi3d.TextureCache()
      texture = ImageSprite.CACHE.create(self.imagename, defer=True)
      self._sprite = pi3d.ImageSprite(texture,
                                          w=texture.ix, h=texture.iy,
                                          shader=Shader.DEFAULT_SHADER,
                                          # shader=Shader.shader(shader),
                                          x=x, y=y, z=z)
      setattr(self._sprite, 'repaint', self.repaint)
      self._add_sprite()
    return self._sprite

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

    if CREATE_SPRITE_IN_CONSTRUCTOR:
      sprite = self.sprite()
    else:
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
    if CREATE_SPRITE_IN_CONSTRUCTOR:
      if self.is_running and self._sprite and not self.sprite_added:
        self.sprite_added = True
        pi3d.Display.Display.INSTANCE.add_sprites(self._sprite)
        print('_add_sprite success')
      else:
        print('_add_sprite FAIL', self.is_running, self._sprite,
              self.sprite_added)
    else:
      pi3d.Display.Display.INSTANCE.add_sprites(self.deferred_sprite)


  def _on_stop(self):
    if CREATE_SPRITE_IN_CONSTRUCTOR:
       if self.sprite_added and self._sprite:
         pi3d.Display.Display.INSTANCE.remove_sprites(self._sprite)
    else:
      pi3d.Display.Display.INSTANCE.remove_sprites(self.deferred_sprite)


