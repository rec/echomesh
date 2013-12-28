from libcpp.string cimport string

cdef extern from "echomesh/color/Colors.h" namespace "echomesh":
  FColor interpolate(FColor begin, FColor end, float ratio)
  void scaleFColorList(FColorList* fc, float scale)
  void combineFColorList(FColorList, FColorList*)

  FColor rgbFromInt(unsigned int argb)
