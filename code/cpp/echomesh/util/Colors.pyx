from libcpp.string cimport string

cdef extern from "echomesh/util/Colors.h" namespace "echomesh":
  bool fillColor(string name, Colour* color)
