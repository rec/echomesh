from __future__ import absolute_import, division, print_function, unicode_literals

import colorsys

from echomesh.graphics import GammaTable

class Model(tuple):
  def __init__(self, values):
    super(Model, self).__init__(values)

  @classmethod
  def from_rgb(cls, r, g, b):
    return cls(*cls.FROM_METHOD(r, g, b))

  def to_rgb(self):
    return RGB(*self.TO_METHOD(*self))

  def __str__(self):
    return '%s(%s)' % (self.__class__.__name__, ', '.join(self))

class RGB(Model):
  FIELDS = set('rgb')
  FROM_METHOD = lambda r, g, b: (r, g, b)
  TO_METHOD = FROM_METHOD

  def __init__(self, r=0.0, g=0.0, b=0.0):
    super(RGB, self).__init__([r, g, b])

class YIQ(Model):
  FIELDS = set('yiq')
  FROM_METHOD = colorsys.yiq_to_rgb
  TO_METHOD = colorsys.rgb_to_yiq

  def __init__(self, y=0.0, i=0.0, q=0.0):
    super(YIQ, self).__init__([y, i, q])

class HLS(Model):
  FIELDS = set('hls')
  FROM_METHOD = colorsys.hls_to_rgb
  TO_METHOD = colorsys.rgb_to_hls

  def __init__(self, h=0.0, l=1.0, s=1.0):
    super(HLS, self).__init__([h, l, s])

class HSV(Model):
  FIELDS = set('hsv')
  FROM_METHOD = colorsys.hsv_to_rgb
  TO_METHOD = colorsys.rgb_to_hsv

  def __init__(self, h=0.0, s=1.0, v=1.0):
    super(HSV, self).__init__([h, s, v])


CLASSES = [RGB, YIQ, HLS, HSV]

def get_model(color):
  fields = set(color.iterkeys())
  for cl in CLASSES:
    cl_fields = getattr(cl, 'FIELDS')
    if (fields & cl_fields) and not (fields - cl_fields):
      return cl
    elif not fields & cl_fields:
      print('not 1', fields, cl_fields)
    else:
      print('not 2')

def make_color(color):
  model = get_model(color)
  return model and model(*color)
