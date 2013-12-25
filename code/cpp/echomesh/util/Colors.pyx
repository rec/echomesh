from libcpp.string cimport string

ctypedef vector[Colour] ColourList

cdef extern from "echomesh/util/Colors.h" namespace "echomesh":
  bool fillColor(string name, Colour* color)
  Colour colorFromInt(unsigned int argb)
  void copyColor(Colour c1, Colour* c2)
  string colorName(Colour color)
  void sortColourList(ColourList*)
  int compareColors(Colour x, Colour y)
  int countColorsInList(ColourList, Colour)
  int indexColorInList(ColourList, Colour)
  void reverseColourList(ColourList*)
  void fillColourList(ColourList*, Colour begin, Colour end, int size)
  Colour interpolate(Colour begin, Colour end, int index, int size)

