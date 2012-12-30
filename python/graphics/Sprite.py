from __future__ import absolute_import, division, print_function, unicode_literals

import os.path
import time

from pi3d.shape import Sprite
from pi3d.context.Light import Light
from pi3d.Camera import Camera
from pi3d.Shader import Shader

from graphics.Pi3dDisplay import PI3D_DISPLAY  # TODO: remove this.

from util.Envelope import Envelope
from util import Log
from util.Openable import Openable

LOGGER = Log.logger(__name__)
DISPLAY = PI3D_DISPLAY.display

DEFAULT_Z = -2.0

CAMERA = Camera((0, 0, 0), (0, 0, -0.1),
                (1, 1000, DISPLAY.win_width/1000.0, DISPLAY.win_height/1000.0))
LIGHT = Light((10, 10, -20))
SHADER = None  # Shader('shaders/uv_flat')


class ImageSprite(Sprite.ImageSprite, Openable):
  def __init__(self, file=None, loops=1,
               position=(0, 0), rotation=0, size=1, duration=0, z=DEFAULT_Z):
    Openable.__init__(self)
    self._imagename = file
    LOGGER.debug('Opening sprite %s', self._imagename)

    self._loops = loops
    self._loop_number = 0
    self._position = Envelope(position)
    self._rotation = Envelope(rotation)
    self._size = Envelope(size)
    self._z = Envelope(z)

    x, y, z = self.coords(0)
    texture = PI3D_DISPLAY.load_texture(file)
    Sprite.ImageSprite.__init__(self, texture,
                                SHADER, camera=CAMERA, light=LIGHT,
                                x=x, y=y, z=z)

    self._time = 0
    if duration:
      self._duration = duration
    else:
      envs = [self._position, self._rotation, self._size]
      self._duration = max(x.length() for x in envs)

    PI3D_DISPLAY.add_sprite(self)

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
        self.close()
        return

    self.position(*self.coords(elapsed))
    size = self._size.interpolate(elapsed)
    self.scale(size, size, size)
    self.rotateToZ(self._rotation.interpolate(elapsed))

    self.draw()
