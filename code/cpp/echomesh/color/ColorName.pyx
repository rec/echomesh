cdef extern from "echomesh/color/ColorName.h" namespace "echomesh::color":
  string rgbToName(FColor color)
  bool nameToRgb(string name, FColor* color)

