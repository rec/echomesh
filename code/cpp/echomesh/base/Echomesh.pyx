cdef extern from "echomesh/base/Echomesh.h" namespace "echomesh":
  cdef cppclass Point:
    Point(int x, int y)

