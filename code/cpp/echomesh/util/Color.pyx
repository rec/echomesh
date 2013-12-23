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
    return [self.thisptr.getFloatRed(),
            self.thisptr.getFloatGreen(),
            self.thisptr.getFloatBlue()]

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

  def __str__(self):
    return 'Color(%s)' % colorName(self.thisptr[0])

  def __repr__(self):
    return self.__str__()
