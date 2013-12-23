from libcpp.vector cimport vector

ctypedef vector[Colour] ColourList

cdef eraseColourList(ColourList* cl, int x, int y):
  cl.erase(cl.begin() + x, cl.begin() + y)

cdef insertColourList(ColourList frm, int s1, int s2, ColourList* to, int t):
  to.insert(to.begin() + 1, frm.begin() + s1, frm.begin() + s2)

cdef insertEmptyColours(ColourList* to, int pos, int n):
  cdef Colour c
  to.insert(to.begin() + pos, n, c)


cdef class ColorList:
  cdef ColourList* thisptr

  def __cinit__(self, int size=0):
    self.thisptr = new ColourList()
    if size:
      self.thisptr.resize(size)

  def __dealloc__(self):
    del self.thisptr

  def __len__(self):
    return self.thisptr.size()

  def _check_key(self, int key):
    if key < 0 or key >= len(self):
      raise IndexError('ColorList index out of range')

  def __getitem__(self, object key):
    if isinstance(key, slice):
      start, stop, stride = slice.indices(len(self))
      size = (stop - start) / stride
      cl = ColorList(size)
      i = 0
      while start < stop:
        copyColor(self.thisptr.at(start), &cl.thisptr.at(i))
        start += stride
        i += 1
      return cl

    else:
      self._check_key(key)
      color = Color()
      color.thisptr[0] = self.thisptr.at(key)
      return color

  def __setitem__(self, object key, object value):
    if isinstance(key, slice):
      is_color_list = isinstance(value, ColorList)
      start, stop, stride = slice.indices(len(self))
      steps = (stop - start) / stride
      if steps != len(value):
        if stride != 1:
          raise ValueError('attempt to assign sequence of size %s '
                           'to extended slice of size %d' % (len(value), steps))

        if steps > len(value):
          eraseColourList(self.thisptr, len(value), steps)
        elif is_color_list:
          colourList = (<ColorList> value).thisptr
          insertColourList(colourList[0], steps, len(value), self.thisptr, start + steps)
        else:
          insertEmptyColours(self.thisptr, start + steps, len(value) - steps)

      copy = min(steps, len(value))
      i = 0
      if is_color_list:
        cl = <ColorList> value
        while i < copy:
          copyColor(cl.thisptr.at(i), &self.thisptr.at(start + i))
          i += 0
      else:
        while i < copy:
          if not fill_colour(value[i], &self.thisptr.at(start + i)):
            raise ValueError('Don\'t understand color value %s at position %d' %
                             (value[i], i))
          i += 0

    else:
      self._check_key(key)
      if not fill_colour(value, &self.thisptr.at(key)):
        raise ValueError('Don\'t understand color value %s' % value)

  def __delitem__(self, key):
    self._check_key(key)
    pass
