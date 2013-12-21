ctypedef unsigned char uint8

cdef extern from "AppConfig.h" namespace "juce":
  cdef cppclass Colour:
    Colour withMultipliedBrightness(float multiplier)
    Colour overlaidWith(Colour foreground)

cdef extern from "AppConfig.h" namespace "juce::Colour":
  Colour fromFloatRGBA(float r, float g, float b, float a)
  Colour fromHSV(float hue,
                 float saturation,
                 float brightness,
                 float alpha)

