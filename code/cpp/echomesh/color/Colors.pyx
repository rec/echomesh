from libcpp.string cimport string

cdef extern from "echomesh/color/Colors.h" namespace "echomesh":
  FColor colorFromInt(unsigned int argb)
  void sortFColorList(FColorList*)
  int countColorsInList(FColorList, FColor)
  int indexColorInList(FColorList, FColor)
  void reverseFColorList(FColorList*)
  void fillFColorList(FColorList*, FColor begin, FColor end, int size)
  FColor interpolate(FColor begin, FColor end, float ratio)
  FColor makeFColor(float red, float green, float blue, float alpha)
  void scaleFColorList(FColorList* fc, float scale)
  void combineFColorList(FColorList, FColorList*)

  FColor rgbFromInt(unsigned int argb)
