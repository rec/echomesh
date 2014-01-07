include "echomesh/color/FColor.pyx"
include "echomesh/color/HSB.pyx"
include "echomesh/color/ColorModel.pyx"
include "echomesh/color/ColorName.pyx"

import six

_EPSILON = (1.0 / 2 ** 16)

def _near_zero(x):
  print('_near_zero', x, _EPSILON)
  return abs(x) < _EPSILON

_COLOR_COMPARES = {
  0: lambda x: x > 0,
  1: lambda x: x >= 0,
  2: lambda x: x == 0,
  3: lambda x: x != 0,
  4: lambda x: x < 0,
  5: lambda x: x <= 0,
  }

cdef bool richcmpColors(FColor* x, FColor* y, int cmp):
  result = _COLOR_COMPARES[cmp](x.compare(y[0]))
  return result

cdef class Color:
  cdef FColor* thisptr

  def __cinit__(self, object args=None):
    self.thisptr = new FColor()
    if not fill_color(args, self.thisptr):
      raise ValueError('Can\'t construct color from "%s"' % str(args))

  @property
  def rgb(self):
    return [self.thisptr.red(), self.thisptr.green(), self.thisptr.blue()]

  @property
  def hsb(self):
    cdef FColor c
    cdef float* parts
    c = hsbFromRgb(self.thisptr[0])
    return [c.red(), c.green(), c.blue()]

  @property
  def alpha(self):
    return self.thisptr.alpha()

  @property
  def red(self):
    return self.rgb[0]

  @property
  def green(self):
    return self.rgb[1]

  @property
  def blue(self):
    return self.rgb[2]

  def scale(self, float f):
    self.thisptr.scale(f)

  def combine(self, Color c):
    self.thisptr.combine(c.thisptr[0])

  def __dealloc__(self):
    del self.thisptr

  def __len__(self):
    return 3

  def __getitem__(self, object key):
    return self.rgb[key]

  def __repr__(self):
    return 'Color(%s)' % str(self)

  def __richcmp__(Color self, Color other, int cmp):
    return richcmpColors(self.thisptr, other.thisptr, cmp)

  def __str__(self):
    return rgbToName(self.thisptr[0])


cdef bool fill_color(object x, FColor* c):
  if not x:
    c.copy(FColor(0.0, 0.0, 0.0, 1.0))
    return True

  if isinstance(x, Color):
    c.copy((<Color> x).thisptr)
    return True

  elif isinstance(x, six.string_types):
    return nameToRgb(x, c)

  if isinstance(x, six.integer_types):
    c.copy(FColor(x))
    return True

  try:
    if len(x) == 3:
      c.copy(FColor(x[0], x[1], x[2], 1.0))
      return True

    if len(x) == 4:
      c.copy(FColor(x[0], x[1], x[2], x[3]))
      return True
  except:
    pass
