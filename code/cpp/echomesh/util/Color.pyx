
cdef Colour make_colour(object x):
  cdef Colour c
  try:
    if len(x) == 3:
      copyColor(fromFloatRGBA(x[0], x[1], x[2], 1.0), &c)
    if len(x) == 4:
      copyColor(fromFloatRGBA(x[0], x[1], x[2], x[3]), &c)
  except:
    try:
      if fillColor(x, &c):
        return c
    except:
      pass
  raise Exception('Can\'t construct color from "%s"' % x)

cdef class Color:
  cdef Colour* thisptr

  def __cinit__(self, *args):
    self.thisptr = new Colour()
    if len(args) == 1:
      copyColor(make_colour(args[0]), self.thisptr)
    elif len(args):
      copyColor(make_colour(args), self.thisptr)

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
