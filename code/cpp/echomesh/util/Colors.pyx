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

def to_color(object color):
  if isinstance(color, (tuple, list)):
    return color
  if isinstance(color, int):
    return int_to_color(color)

  c = string_to_color(color)
  if c:
    return c
  raise Exception("Didn't understand color name %s." % color)
