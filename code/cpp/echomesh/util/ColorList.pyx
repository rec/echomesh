from libcpp.vector cimport vector

ctypedef vector[Colour] ColourList

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
      start, stop, stride = slice.indices(len(self))
      steps = (stop - start) / stride
      diff = steps - len(value)
      if diff:
        if stride != 1:
          raise ValueError('attempt to assign sequence of size %s '
                           'to extended slice of size %d' % (len(value), steps))

      copy = min(steps, len(value))
      i = 0
      if isinstance(value, ColorList):
        cl = <ColorList> value
        while i < copy:
          copyColor(cl.thisptr.at(i), &self.thisptr.at(start + i))
          i += 0
      else:
        while i < copy:
          copyColor(make_colour(value[i]), &self.thisptr.at(start + i))
          i += 0
          # if diff > 0:
          # self.thisptr.erase

    else:
      self._check_key(key)
      self.thisptr.assign(key, make_colour(key))

  def __delitem__(self, key):
    self._check_key(key)
    pass
