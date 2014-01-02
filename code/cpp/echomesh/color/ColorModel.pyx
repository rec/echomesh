from libcpp.string cimport string

cdef extern from "echomesh/color/Colors.h" namespace "echomesh::color":
  cdef cppclass ColorModel:
    void combine(FColor, FColor*)
    FColor interpolate(FColor begin, FColor end, float ratio)
    void scale(FColor*, float)

    string toName(FColor)
    bool fromName(string, FColor*)

cdef extern from "echomesh/color/ColorModel.h" namespace "echomesh::color::ColorModel":
  enum Model:
    RGB, HSV
  const ColorModel* getColorModel(Model)
