include "echomesh/color/FColor.pyx"
include "echomesh/color/HSB.pyx"
include "echomesh/color/ColorModel.pyx"
include "echomesh/color/ColorName.pyx"

import six

_EPSILON = (1.0 / 2 ** 16)

def _near_zero(x):
  print('_near_zero', x, _EPSILON)
  return abs(x) < _EPSILON

COMPARE_MAP = {
  0: lambda x: x > 0,
  1: lambda x: x >= 0,
  2: lambda x: x == 0,
  3: lambda x: x != 0,
  4: lambda x: x < 0,
  5: lambda x: x <= 0,
  }

def compare_ints(int x, int y, int comparer):
  return COMPARE_MAP[comparer](cmp(x, y))

cdef bool richcmpColors(const FColor* x, const FColor* y, int cmp):
  return COMPARE_MAP[cmp](x.compare(y[0]))

cdef class Color:
  cdef FColor* thisptr

  def __cinit__(self, object args=None):
    self.thisptr = new FColor()
    if not fill_color(args, self.thisptr):
      raise ValueError('Can\'t construct color from "%s"' % str(args))

  @property
  def rgb(self):
    return [self.thisptr.red(), self.thisptr.green(), self.thisptr.blue()]

  def rgb_range(self, begin, end):
    """Return the RGB components as integers in the interval [begin, end)."""
    width = end  - begin
    def scale(f):
      return min(end - 1, int(begin + f * width))
    return tuple(scale(f) for f in self.rgb)

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

  def gamma(self, float f):
    self.thisptr.gamma(f)

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

def _conv(c):
  return c if isinstance(c, float) else c / 256.0;

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
      c.copy(FColor(_conv(x[0]), _conv(x[1]), _conv(x[2]), 1.0))
      return True

    if len(x) == 4:
      c.copy(FColor(_conv(x[0]), _conv(x[1]), _conv(x[2]), _conv(x[3])))
      return True
  except:
    pass
