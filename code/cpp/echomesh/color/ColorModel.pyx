import six

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
    RGB, HSB
  const ColorModel* getColorModel(Model)

cdef const ColorModel* get_color_model(object x):
  if (x or RGB) in [RGB, HSB]:
    return getColorModel(x or RGB)
  x = x.lower()
  if x == 'rgb':
    return getColorModel(RGB)
  if x == 'hsv':
    return getColorModel(HSB)
  return NULL
