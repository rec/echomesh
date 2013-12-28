include "echomesh/color/FColorList.pyx"

import math

def _make_list(object value):
  try:
    len(value)
  except:
    value = list(value)
  return value

cdef class ColorList:
  cdef FColorList* thisptr

  def __cinit__(self, args=None):
    self.thisptr = new FColorList()
    if args:
      self.extend(args)

  def __dealloc__(self):
    del self.thisptr

  def append(self, object item):
    cdef FColor c
    if fill_color(item, &c):
      self.thisptr.push_back(c)
    else:
      raise ValueError('Don\'t understand color value %s' % item)

  def combine(self, object other):
    cdef ColorList cl
    if isinstance(other, ColorList):
      cl = <ColorList> other
    else:
      cl = ColorList(other)
    combineFColorList(cl.thisptr[0], self.thisptr)

  def count(self, object item):
    cdef FColor c
    if not fill_color(item, &c):
      raise ValueError('Don\'t understand color value %s' % item)
    return self.thisptr.count(c)

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
    cdef FColor c
    if not fill_color(item, &c):
      raise ValueError('Don\'t understand color value %s' % item)
    index = self.thisptr.index(c)
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
    self.thisptr.reverse()

  def scale(self, float scale):
    scaleFColorList(self.thisptr, scale)

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
      parts = range(*key.indices(len(self)))
      cl = ColorList()
      cl.thisptr.resize(len(parts))
      i = 0
      for j in parts:
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
      if not richcmpColors(self.thisptr.at(i), other.thisptr.at(i), cmp):
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
          self.thisptr.eraseRange(length, slice_length)
        else:
          self.thisptr.insertRange(indices[0] + slice_length,
                                   cl.thisptr[0], slice_length, length)

      i = 0
      for j in parts:
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

def force_color(c):
  return c if isinstance(c, Color) else Color(c)

def color_spread(*args):
  cdef Color c1
  cdef Color c2
  if len(args) < 3:
    raise Exception('make_color_spread must have at least three arguments')

  if not len(args) % 2:
    raise Exception('make_color_spread must have an odd number of arguments')

  colors = [force_color(a) for a in args[::2]]
  steps = args[1::2]

  cl = ColorList()
  cl.thisptr.resize(sum(steps) + len(colors))
  pos = 0
  for i, step in enumerate(steps):
    c1, c2 = colors[i:i+2]
    for j in range(step + 2):
      inc = j / (step + 1.0)
      cl.thisptr.set(c1.thisptr.interpolate(c2.thisptr[0], inc), pos)
      pos += 1
    pos -= 1
  return cl

def even_color_slots(int size, int slots):
  slot = 0
  for i in range(slots):
    previous = slot
    slot = int(math.ceil(((i + 1) * size) / slots))
    yield slot - previous - 1

def even_color_spread(size, *colors):
  slots = list(even_color_slots(size - 1, len(colors) - 1))
  args = [j for i in zip(colors, slots) for j in i] + [colors[-1]]
  return color_spread(*args)
