from libcpp.string cimport string

cdef extern from "AppConfig.h" namespace "juce::Colours":
  Colour findColourForName(string name, Colour defaultColour)

