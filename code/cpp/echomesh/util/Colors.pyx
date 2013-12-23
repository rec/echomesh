from libcpp.string cimport string

cdef extern from "echomesh/util/Colors.h" namespace "echomesh":
  bool fillColor(string name, Colour* color)
  Colour colorFromInt(unsigned int argb)
  void copyColor(Colour c1, Colour* c2)
  string colorName(Colour color)
