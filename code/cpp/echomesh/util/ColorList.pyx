from libcpp.vector cimport vector

ctypedef vector[Colour] ColourList

cdef class Color:
  cdef Colour* thisptr

  def __cinit__(self):
    self.thisptr = new Colour()

  def __dealloc__(self):
    del self.thisptr

  def from_rgb(self, float r=0.0, float g=0.0, float b=0.0, float a=1.0):
    copyColor(fromFloatRGBA(r, g, b , a), self.thisptr)

  def from_string(self, string s):
    if not fillColor(s, self.thisptr):
      raise Exception('Don\'t understand color name "%s"' % s)


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
      cl = ColorList((stop - start) / stride)
      i = 0
      while start < stop:
        cl.thisptr.assign(i, self.thisptr.at(start))
        start += stride
        i += 1
      return cl

    else:
      self._check_key(key)
      color = Color()
      copyColor(self.thisptr.at(key), color.thisptr)
      return color

  def __setitem__(self, object key, object value):
    if isinstance(key, slice):
      start, stop, stride = slice.indices(len(self))
      cl = ColorList((stop - start) / stride)
      i = 0
      while start < stop:
        cl.thisptr.assign(i, self.thisptr.at(start))
        start += stride
        i += 1

    else:
      self._check_key(key)
      color = Color()
      copyColor(self.thisptr.at(key), color.thisptr)

  def __delitem__(self, key):
    self._check_key(key)
    pass
