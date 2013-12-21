from libcpp.string cimport string

cdef extern from "echomesh/util/Colors.h" namespace "echomesh":
  bool fillColor(string name, Colour* color)
  Colour colorFromInt(unsigned int argb)

def string_to_color(string name):
  cdef Colour color
  if fillColor(name, &color):
    return [color.getFloatRed(), color.getFloatGreen(), color.getFloatBlue()]

def int_to_color(unsigned int argb):
  cdef Colour color = colorFromInt(argb)
  return [color.getFloatRed(), color.getFloatGreen(), color.getFloatBlue()]

