from libcpp.vector cimport vector

cdef eraseColourList(ColourList* cl, int x, int y):
  cl.erase(cl.begin() + x, cl.begin() + y)

cdef insertColourList(ColourList frm, int s1, int s2, ColourList* to, int t):
  to.insert(to.begin() + 1, frm.begin() + s1, frm.begin() + s2)

cdef setColourInList(ColourList* cl, int pos, Colour c):
  copyColor(c, &cl.at(pos))

def _make_list(object value):
  try:
    len(value)
  except:
    value = list(value)
  return value

cdef class ColorList:
  cdef ColourList* thisptr

  def __cinit__(self, *args):
    self.thisptr = new ColourList()
    if len(args) == 1:
      self.extend(args[0])
    elif args:
      raise TypeError('ColorList takes at most 1 argument (%d given)' % len(args))

  def __dealloc__(self):
    del self.thisptr

  def __len__(self):
    return self.thisptr.size()

  def _check_key(self, int key):
    if key < 0 or key >= len(self):
      raise IndexError('ColorList index out of range')

  def resize(self, size):
    if size < 0:
      raise ValueError('ColorList size must be non-negative.')
    self.thisptr.resize(size)

  def _set_item(self, int i, object item):
    cdef Colour c
    if fill_colour(item, &c):
      setColourInList(self.thisptr, i, c)
    else:
      raise ValueError('Don\'t understand color value %s' % item)

  def append(self, object item):
    cdef Colour c
    if fill_colour(item, &c):
      self.thisptr.push_back(c)
    else:
      raise ValueError('Don\'t understand color value %s' % item)

  def extend(self, object items):
    length = len(self)
    items = _make_list(items)
    new_length = len(items)

    self.thisptr.reserve(length + new_length)
    try:
      for item in items:
        self.append(item)
    except:
      self.resize(length)

  def sort(self):
    sortColorList(self.thisptr)

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
      value = _make_list(value)
      if isinstance(value, ColorList):
        cl = <ColorList> value
      else:
        cl = ColorList(value)

      length = len(cl)
      start, stop, stride = key.indices(len(self))
      slice_length = int((stop - start) / stride)

      if slice_length != length:
        if stride != 1:
          raise ValueError('attempt to assign sequence of size %s '
                           'to extended slice of size %d' %
                           (length, slice_length))

        if slice_length > length:
          eraseColourList(self.thisptr, length, slice_length)
        else:
          insertColourList(cl.thisptr[0], slice_length, length, self.thisptr,
                           start + slice_length)

      for i in range(length):
        assert start < stop
        copyColor(cl.thisptr.at(i), &self.thisptr.at(start))
        start += stride

    else:
      self._check_key(key)
      if not fill_colour(value, &self.thisptr.at(key)):
        raise ValueError('Don\'t understand color value %s' % value)

  def __str__(self):
    return '[%s]' % ', '.join(str(c) for c in self)

  def __repr__(self):
    return 'ColorList(%s)' % self.__str__()

  def __delitem__(self, key):
    self._check_key(key)
    pass
