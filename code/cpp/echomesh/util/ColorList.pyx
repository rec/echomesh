from libcpp.vector cimport vector

cdef eraseColourList(ColourList* cl, int x, int y):
  cl.erase(cl.begin() + x, cl.begin() + y)

cdef insertColourList(ColourList frm, int s1, int s2, ColourList* to, int t):
  to.insert(to.begin() + t, frm.begin() + s1, frm.begin() + s2)

cdef setColourInList(ColourList* cl, int pos, Colour c):
  copyColor(c, &cl.at(pos))

cdef eraseInList(ColourList* cl, int pos):
  cl.erase(cl.begin() + pos)

cdef richcmpColorsInList(ColourList* x, ColourList *y, int index, int cmp):
  return richcmpColors(x.at(index), y.at(index), cmp)

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

  def append(self, object item):
    cdef Colour c
    if fill_colour(item, &c):
      self.thisptr.push_back(c)
    else:
      raise ValueError('Don\'t understand color value %s' % item)

  def count(self, object item):
    cdef Colour c
    if not fill_colour(item, &c):
      raise ValueError('Don\'t understand color value %s' % item)
    return countColorsInList(self.thisptr[0], c)

  def extend(self, object items):
    length = len(self)
    items = _make_list(items)
    new_length = len(items)

    self.thisptr.reserve(length + new_length)
    try:
      for item in items:
        self.append(item)
    except:
      self.thisptr.resize(length)

  def index(self, object item):
    cdef Colour c
    if not fill_colour(item, &c):
      raise ValueError('Don\'t understand color value %s' % item)
    index = indexColorInList(self.thisptr[0], c)
    if index >= 0:
      return index
    raise ValueError('%s is not in ColorList' % item)

  def insert(self, int index, object item):
    self[index:index] = [item]

  def pop(self, int index=-1):
    index = self._check_key(index)
    item = self[index]
    del self[index]
    return item

  def remove(self, object item):
    del self[self.index(item)]

  def reverse(self):
    reverseColorList(self.thisptr)

  def sort(self):
    sortColorList(self.thisptr)

  def __add__(self, object other):
    cl = ColorList(self)
    cl.extend(other)
    return cl

  def __contains__(self, object item):
    try:
      self.index(item)
      return True
    except ValueError:
      return False

  def __delitem__(self, key):
    eraseInList(self.thisptr, self._check_key(key))

  def __getitem__(self, object key):
    if isinstance(key, slice):
      parts = range(*key.indices(len(self)))
      cl = ColorList()
      cl.thisptr.resize(len(parts))
      i = 0
      for j in parts:
        copyColor(self.thisptr.at(j), &cl.thisptr.at(i))
        i += 1
      return cl

    else:
      key = self._check_key(key)
      color = Color()
      color.thisptr[0] = self.thisptr.at(key)
      return color

  def __iadd__(self, object other):
    self.extend(other)
    return self

  def __imul__(self, int mult):
    length = len(self)
    self.thisptr.reserve(mult * length)
    for i in range(1, mult):
      insertColourList(self.thisptr[0], 0, length, self.thisptr, i * length)
    return self

  def __len__(self):
    return self.thisptr.size()

  def __mul__(self, int mult):
    cl = ColorList(self)
    cl *= mult
    return cl

  def __radd__(self, object other):
    return ColorList(other) + self

  def __repr__(self):
    return 'ColorList(%s)' % self.__str__()

  def __richcmp__(self, ColorList other, int cmp):
    return self._richcmp(other, cmp)

  def _richcmp(self, ColorList other, int cmp):
    if len(self) != len(other):
      return False
    for i in range(len(self)):
      if not richcmpColorsInList(self.thisptr, other.thisptr, i, cmp):
        return False
    return True

  def __reversed__(self):
    cl = ColorList(self)
    cl.reverse()
    return cl

  def __rmul__(self, int other):
    return self * other

  def __setitem__(self, object key, object value):
    if isinstance(key, slice):
      value = _make_list(value)
      if isinstance(value, ColorList):
        cl = <ColorList> value
      else:
        cl = ColorList(value)

      length = len(cl)
      indices = key.indices(len(self))
      parts = range(*indices)
      slice_length = len(parts)

      if slice_length != length:
        if indices[2] != 1:
          raise ValueError('attempt to assign sequence of size %s '
                           'to extended slice of size %d' %
                           (length, slice_length))

        if slice_length > length:
          eraseColourList(self.thisptr, length, slice_length)
        else:
          insertColourList(cl.thisptr[0], slice_length, length, self.thisptr,
                           indices[0] + slice_length)

      i = 0
      for j in parts:
        copyColor(cl.thisptr.at(i), &self.thisptr.at(j))

    else:
      key = self._check_key(key)
      if not fill_colour(value, &self.thisptr.at(key)):
        raise ValueError('Don\'t understand color value %s' % value)

  def __sizeof__(self):
    return super(ColorList, self).__sizeof__() + 4 * len(self)

  def __str__(self):
    return '[%s]' % ', '.join(str(c) for c in self)

  def _check_key(self, int key):
    if key >= 0:
      if key < len(self):
        return key
    else:
      if -key <= len(self):
        return len(self) + key
    raise IndexError('ColorList index out of range')

  def _set_item(self, int i, object item):
    cdef Colour c
    if fill_colour(item, &c):
      setColourInList(self.thisptr, i, c)
    else:
      raise ValueError('Don\'t understand color value %s' % item)

