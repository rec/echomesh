from libcpp.string cimport string

ctypedef float Parts[3]

cdef extern from "echomesh/color/Colors.h" namespace "echomesh":
  cdef cppclass FColor:
    float alpha()
    float* parts()
  void scaleRgb(FColor* color, float scale)
  void combineRgb(FColor, FColor*)

cdef extern from "echomesh/color/Colors.h" namespace "echomesh::FColor":
  FColor NO_COLOR

ctypedef vector[FColor] FColorList

cdef extern from "echomesh/color/ColorName.h" namespace "echomesh::color":
  string rgbToName(FColor color)
  bool nameToRgb(string name, FColor* color)

cdef extern from "echomesh/color/Colors.h" namespace "echomesh":
  FColor colorFromInt(unsigned int argb)
  void copyColor(FColor c1, FColor* c2)
  void sortFColorList(FColorList*)
  int compareColors(FColor x, FColor y)
  int countColorsInList(FColorList, FColor)
  int indexColorInList(FColorList, FColor)
  void reverseFColorList(FColorList*)
  void fillFColorList(FColorList*, FColor begin, FColor end, int size)
  FColor interpolate(FColor begin, FColor end, float ratio)
  FColor makeFColor(float red, float green, float blue, float alpha)
  void scaleFColorList(FColorList* fc, float scale)
  void combineFColorList(FColorList, FColorList*)

cdef extern from "echomesh/color/RGB.h" namespace "echomesh::RGB":
  FColor fromInt(unsigned int argb)
