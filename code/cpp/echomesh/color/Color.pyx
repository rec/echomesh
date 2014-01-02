include "echomesh/color/FColor.pyx"
include "echomesh/color/HSB.pyx"
include "echomesh/color/ColorName.pyx"

import six

_COLOR_COMPARES = {
  0: lambda x: x < 0,
  1: lambda x: x <= 0,
  2: lambda x: x == 0,
  3: lambda x: x != 0,
  4: lambda x: x > 0,
  5: lambda x: x >= 0,
  }

cdef bool richcmpColors(FColor x, FColor y, int cmp):
  return _COLOR_COMPARES[cmp](x.compare(y))

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
    cdef float* parts
    c = self._model.toRgb(self.thisptr[0])
    parts = c.parts()
    return [parts[0], parts[1], parts[2]]

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
    self._model.scale(self.thisptr, f)

  def combine(self, Color c):
    self._model.combine(c.thisptr[0], self.thisptr)

  def __dealloc__(self):
    del self.thisptr

  def __len__(self):
    return 3

  def __getitem__(self, object key):
    return self.rgb[key]

  def __repr__(self):
    return 'Color(%s)' % str(self)

  def __richcmp__(Color self, Color other, int cmp):
    return richcmpColors(self.thisptr[0], other.thisptr[0], cmp)

  def __str__(self):
    return rgbToName(self.thisptr[0])


cdef bool fill_color(object x, FColor* c, const ColorModel* model):
  if not x:
    c.copy(FColor(0.0, 0.0, 0.0, 0.0))
    return True

  if isinstance(x, Color):
    cl = <Color> x
    if cl._model == model:
      c.copy(cl.thisptr)
    return True

  elif isinstance(x, six.string_types):
    return model.fromName(x, c)

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
