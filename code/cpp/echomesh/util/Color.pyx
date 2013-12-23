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

  def __str__(self):
    return 'Color(%s)' % colorName(self.thisptr[0])

  def __repr__(self):
    return self.__str__()

  @property
  def red(self):
    return self.thisptr.getFloatRed()

  @property
  def green(self):
    return self.thisptr.getFloatGreen()

  @property
  def blue(self):
    return self.thisptr.getFloatBlue()

