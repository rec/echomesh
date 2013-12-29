from libcpp.string cimport string

cdef extern from "echomesh/color/Colors.h" namespace "echomesh::color":
  void scaleFColorList(FColorList* fc, float scale)
  void combineFColorList(FColorList, FColorList*)

cdef extern from "echomesh/color/Colors.h" namespace "echomesh::color::RGB":
  void scaleRGB(FColor* color, float scale)
  void combineRGB(FColor x, FColor* y)
