cdef extern from "echomesh/color/Transform.h" namespace "echomesh::color":
  cdef cppclass CTransform:
    float apply(float x)
    float inverse(float x)

  cdef CTransform* makeTransform(string)

cdef class Transform:
  cdef CTransform* thisptr

  def __cinit__(self, object s):
    if not isinstance(s, six.string_types):
      raise ValueError('Transform description "%s" is not a string' % s)

    self.thisptr = makeTransform(s)
    if not self.thisptr:
      raise ValueError('Couldn\'t understand transform %s' % s)

  def __dealloc__(self):
    del self.thisptr

  def apply(self, float x):
    return self.thisptr.apply(x)

  def inverse(self, float x):
    return self.thisptr.inverse(x)

