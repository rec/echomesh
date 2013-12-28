cdef extern from "echomesh/color/Colors.h" namespace "echomesh":
  cdef cppclass FColor:
    float alpha()
    float* parts()
    bool compare(FColor)

  void scaleRgb(FColor* color, float scale)
  void combineRgb(FColor, FColor*)

cdef extern from "echomesh/color/Colors.h" namespace "echomesh::FColor":
  FColor NO_COLOR
