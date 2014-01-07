import six

from libcpp.string cimport string

cdef extern from "echomesh/color/ColorModel.h" namespace "echomesh::color":
  cdef cppclass ColorModel:
    FColor interpolate(FColor begin, FColor end, float ratio)
    string modelName()
    FColor toRgb(FColor)
    FColor fromRgb(FColor)
    bool isRgb()

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
  if x == 'hsb':
    return getColorModel(HSB)
  print('Error: didn\t understand model %s: returning RGB' % x)
  return getColorModel(RGB)
