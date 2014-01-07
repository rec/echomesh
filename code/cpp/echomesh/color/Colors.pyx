include "echomesh/color/ColorModel.pyx"

from libcpp.string cimport string

cdef extern from "echomesh/color/Colors.h" namespace "echomesh::color":
  void combineFColorList(FColorList, FColorList*)

