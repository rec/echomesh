from libcpp.string cimport string

cdef extern from "echomesh/color/Colors.h" namespace "echomesh::color":
  cdef cppclass ColorModel:
    void scale(FColor*, float)
    void combine(FColor, FColor*)
    string toName(FColor)
    bool fromName(string, FColor*)

cdef extern from "echomesh/color/ColorModel.h" namespace "echomesh::color::ColorModel":
  ColorModel* RGB_MODEL
  ColorModel* HSB_MODEL
