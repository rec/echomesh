from libcpp.vector cimport vector

ctypedef vector[Colour] ColourList

cdef class Color:
  cdef Colour* thisptr

  def __cinit__(self):
    self.thisptr = new Colour()

  def __dealloc__(self):
    del self.thisptr


cdef class ColorList:
  cdef ColourList* thisptr

  def __cinit__(self):
    self.thisptr = new ColourList()

  def __dealloc__(self):
    del self.thisptr

  def __len__(self):
    return self.thisptr.size()

  def __getitem__(self, key):
    pass

  def __setitem__(self, key, value):
    pass

  def __delitem__(self, key):
    pass

  def __iter__(self):
    pass

  def __reversed__(self):
    pass

  def __contains__(self, item):
    pass
