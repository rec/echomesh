include "echomesh/color/FColorList.pyx"

import math
import six

def _make_list(object value):
  try:
    len(value)
  except:
    value = list(value)
  return value

cdef ColorList toColorList(object value):
  if isinstance(value, ColorList):
    return <ColorList> value
  else:
    return ColorList(value)

def to_color_list(object x):
  return toColorList(x)


cdef class ColorList:
  cdef FColorList* thisptr

  def __cinit__(self, colors=None):
    self.thisptr = new FColorList()
    self.extend(colors)

  def __dealloc__(self):
    del self.thisptr

  def append(self, object item):
    cdef FColor c
    if fill_color(item, &c):
      self.thisptr.push_back(c)
    else:
      raise ValueError('Don\'t understand color value %s' % item)

  def combine(self, *items):
    cdef ColorList cl
    for other in items:
      cl = toColorList(other)
      for i in range(self.thisptr.size()):
        self.thisptr.at(i).combine(cl.thisptr.at(i))

  def count(self, object item):
    cdef FColor c
    if not fill_color(item, &c):
      raise ValueError('Don\'t understand color value %s' % item)
    return self.thisptr.count(c)

  def extend(self, object colors, bool return_errors=False):
    if not colors:
      return

    if isinstance(colors, ColorList):
      self.thisptr.extend((<ColorList> colors).thisptr[0])
      return

    original_length = len(self)
    colors = list(colors)
    new_length = len(colors)
    if return_errors:
      error_colors = []

    self.thisptr.reserve(original_length + new_length)
    for color in colors:
      try:
        self.append(color)
      except:
        if return_errors:
          error_colors.append(color)
          self.append(None)
        else:
          self.thisptr.resize(original_length)
          raise
    return return_errors and error_colors

  def gamma(self, float f):
    self.thisptr.gamma(f)

  def index(self, object color):
    cdef FColor c
    if not fill_color(color, &c):
      raise ValueError('Don\'t understand color value %s' % color)
    index = self.thisptr.index(c)
    if index >= 0:
      return index
    raise ValueError('%s is not in ColorList' % color)

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
    self.thisptr.reverse()

  def scale(self, float s):
    self.thisptr.scale(s)

  def set_all(self, Color c):
    self.thisptr.setAll(c.thisptr[0])

  def sort(self):
    self.thisptr.sort()

  def __add__(self, object other):
    cl = ColorList(self)
    cl.extend(other)
    return cl

  def __contains__(self, object item):
    try:
      self.index(item)
      return True
    except:
      return False

  def __delitem__(self, key):
    self.thisptr.eraseOne(self._check_key(key))

  def __getitem__(self, object key):
    if isinstance(key, slice):
      indices = range(*key.indices(len(self)))
      cl = ColorList()
      cl.thisptr.resize(len(indices))
      i = 0
      for j in indices:
        cl.thisptr.set(self.thisptr.at(j), i)
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
      self.thisptr.insertRange(i * length, self.thisptr[0], 0, length)
    return self

  def __len__(self):
    return self.thisptr.size()

  def __mul__(self, object mult):
    if not isinstance(self, ColorList):
      self, mult = mult, self
    cl = ColorList(self)
    cl *= mult
    return cl

  def __radd__(self, object other):
    return ColorList(other) + self

  def __repr__(self):
    return 'ColorList(%s)' % self.__str__()

  def __richcmp__(ColorList self, ColorList other, int cmp):
    if len(self) != len(other):
      return False
    for i in range(len(self)):
      if not richcmpColors(&self.thisptr.at(i), &other.thisptr.at(i), cmp):
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
      cl = toColorList(value)
      length = len(cl)
      indices = key.indices(len(self))
      pieces = range(*indices)
      slice_length = len(pieces)

      if slice_length != length:
        if indices[2] != 1:
          raise ValueError('attempt to assign sequence of size %s '
                           'to extended slice of size %d' %
                           (length, slice_length))

        if slice_length > length:
          self.thisptr.eraseRange(length, slice_length)
        else:
          self.thisptr.insertRange(indices[0] + slice_length,
                                   cl.thisptr[0], slice_length, length)

      i = 0
      for j in pieces:
        self.thisptr.set(cl.thisptr.at(i), j)

    else:
      key = self._check_key(key)
      if not fill_color(value, &self.thisptr.at(key)):
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
    cdef FColor c
    if fill_color(item, &c):
      self.thisptr.set(c, i)
    else:
      raise ValueError('Don\'t understand color value %s' % item)


def color_list_with_errors(colors=None):
  if isinstance(colors, six.string_types):
    colors = [colors]
  cl = ColorList()
  return cl, cl.extend(colors, return_errors=True)

def combine_color_lists(color_lists):
  cdef ColorList result = ColorList()
  cdef ColorList cl
  result = ColorList()
  for cl in color_lists:
    pass
