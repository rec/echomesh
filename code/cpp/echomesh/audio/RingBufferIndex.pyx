cdef extern from "echomesh/audio/RingBufferIndex.h" namespace "echomesh::audio":
  cdef cppclass RingBufferIndex[Number]:
    RingBufferIndex(Number size)
    RingBufferIndex(Number size, Number begin, Number end)
    vector[pair[Number, Number]] write(Number size)
    vector[pair[Number, Number]] read(Number size)

    Number available()
    Number begin()
    Number end()
    Number size()

cdef class PyRingBufferIndex:
  cdef RingBufferIndex[int]* thisptr

  def __cinit__(self, int size, int begin=0, int end=0):
    self.thisptr = new RingBufferIndex[int](size, begin, end)

  def __dealloc__(self):
    del self.thisptr

  def read(self, int count):
    return self.thisptr.read(count)

  def write(self, int count):
    return self.thisptr.write(count)

  def available(self):
    return self.thisptr.available()

  def begin(self):
    return self.thisptr.begin()

  def end(self):
    return self.thisptr.end()

  def size(self):
    return self.thisptr.size()
