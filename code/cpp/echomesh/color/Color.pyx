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
  cdef const ColorModel* _model

  def __cinit__(self, object args=None, object model=RGB):
    self.thisptr = new FColor()
    self._model = get_color_model(model)
    if not fill_color(args, self.thisptr, self._model):
      raise ValueError('Can\'t construct color from "%s"' % str(args))

  @property
  def rgb(self):
    cdef FColor c
    c = self._model.toRgb(self.thisptr[0])
    return [c.red(), c.green(), c.blue()]

  @property
  def hsb(self):
    cdef FColor c
    cdef float* parts
    m = self.model
    if self._model.isRgb():
      c = hsbFromRgb(self.thisptr[0])
      return [c.red(), c.green(), c.blue()]
    return [self.thisptr.red(), self.thisptr.green(), self.thisptr.blue()]

  @property
  def alpha(self):
    return self.thisptr.alpha()

  @property
  def model(self):
    return self._model.modelName()

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


cdef bool fill_color(object x, FColor* c, const ColorModel* model):
  if not x:
    c.copy(FColor(0.0, 0.0, 0.0, 1.0))
    return True

  if isinstance(x, Color):
    cl = <Color> x
    if cl._model == model:
      c.copy(cl.thisptr)
    else:
      c.copy(model.fromRgb(cl._model.toRgb(cl.thisptr[0])))
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
