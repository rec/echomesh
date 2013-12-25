import six

cdef bool fill_colour(object x, Colour* c):
  if not x:
    return True
  elif isinstance(x, Color):
    color = <Color> x
    copyColor(color.thisptr[0], c)
  elif isinstance(x, six.string_types):
    return fillColor(x, c)
  elif isinstance(x, six.integer_types):
    copyColor(colorFromInt(x), c)
  else:
    try:
      if len(x) == 3:
        copyColor(fromFloatRGBA(x[0], x[1], x[2], 1.0), c)
      elif len(x) == 4:
        copyColor(fromFloatRGBA(x[0], x[1], x[2], x[3]), c)
      else:
        return False
    except:
      return False
  return True

_COLOR_COMPARES = {
  0: lambda x: x < 0,
  1: lambda x: x <= 0,
  2: lambda x: x == 0,
  3: lambda x: x != 0,
  4: lambda x: x > 0,
  5: lambda x: x >= 0,
  }

cdef bool richcmpColors(Colour x, Colour y, int cmp):
  return _COLOR_COMPARES[cmp](compareColors(x, y))

cdef class Color:
  cdef Colour* thisptr

  def __cinit__(self, *args):
    self.thisptr = new Colour()
    if len(args) == 1:
      args = args[0]
    if not fill_colour(args, self.thisptr):
      raise ValueError('Can\'t construct color from "%s"' % args)

  @property
  def rgb(self):
    t = self.thisptr
    return [t.getFloatRed(), t.getFloatGreen(), t.getFloatBlue()]

  @property
  def red(self):
    return self.thisptr.getFloatRed()

  @property
  def green(self):
    return self.thisptr.getFloatGreen()

  @property
  def blue(self):
    return self.thisptr.getFloatBlue()

  def __dealloc__(self):
    del self.thisptr

  def __int__(self):
    return self.thisptr.getARGB()

  def __str__(self):
    return colorName(self.thisptr[0])

  def __repr__(self):
    return 'Color(%s)' % str(self)

  def __richcmp__(self, Color other, int cmp):
    return self._richcmp(other, cmp)

  def _richcmp(self, Color other, int cmp):
    return richcmpColors(self.thisptr[0], other.thisptr[0], cmp)

def make_color(c):
  return c if isinstance(c, Color) else Color(c)
