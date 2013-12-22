cdef class Color:
  cdef Colour* thisptr

  def __cinit__(self):
    self.thisptr = new Colour()

  def __dealloc__(self):
    del self.thisptr

  def set_from_rgb(self, float r=0.0, float g=0.0, float b=0.0, float a=1.0):
    self.thisptr[0] = fromFloatRGBA(r, g, b , a)

  def set_from_string(self, string s):
    if not fillColor(s, self.thisptr):
      raise Exception('Don\'t understand color name "%s"' % s)

  def set_from_object(self, object x):
    try:
      self.set_from_string(x)
    except:
      try:
        self.set_from_rgb(*x)
      except:
        raise Exception('Can\'t construct color from "%s"' % x)

  def __str__(self):
    return 'Color(%s)' % colorName(self.thisptr[0])

cdef bool fill_color_from_rgba(
    Colour* c, float r=0.0, float g=0.0, float b=0.0, float a=1.0):
  c[0] = fromFloatRGBA(r, g, b, a)

def make_color(object x):
  c = Color()
  c.set_from_object(x)
  return c

cdef Colour make_colour(object x):
  cdef Colour c = Colour()
  try:
    if len(x) == 3:
      fill_color_from_rgba(&c, x[0], x[1], x[2])
      return c
    if len(x) == 4:
      fill_color_from_rgba(&c, x[0], x[1], x[2], x[3])
      return c
  except:
    try:
      if fillColor(x, &c):
        return c
    except:
      pass
  raise Exception('Can\'t construct color from "%s"' % x)
