# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8

ctypedef unsigned int uint

include "juce/juce_graphics/colour/juce_Colour.pyx"
include "juce/juce_graphics/colour/juce_Colours.pyx"

include "echomesh/audio/DefaultDevice.pyx"
include "echomesh/audio/Source.pyx"
include "echomesh/color/Color.pyx"
include "echomesh/color/ColorList.pyx"
include "echomesh/color/ColorSpread.pyx"
include "echomesh/color/Concatenate.pyx"
include "echomesh/color/Insert.pyx"
include "echomesh/color/Mirror.pyx"
include "echomesh/color/SPI.pyx"
include "echomesh/color/Transform.pyx"
include "echomesh/component/LightingWindow.pyx"
include "echomesh/util/EchomeshApplication.pyx"
include "echomesh/util/Log.pyx"
