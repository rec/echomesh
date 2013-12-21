cdef extern from "AppConfig.h" namespace "juce":
  cdef cppclass Colour:
    Colour withMultipliedBrightness(float multiplier)
    Colour overlaidWith(Colour foreground)
    float getFloatRed()
    float getFloatGreen()
    float getFloatBlue()

cdef extern from "AppConfig.h" namespace "juce::Colour":
  Colour fromFloatRGBA(float red, float green, float blue, float alpha)
  Colour fromHSV(float hue, float saturation, float brightness, float alpha)

