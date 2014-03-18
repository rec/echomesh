# distutils: language = c++
# cython: c_string_type=unicode, c_string_encoding=utf8

ctypedef unsigned int uint

from libcpp cimport bool
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.pair cimport pair

cdef extern from "Python.h":
   char* PyByteArray_AsString(object bytearray) except NULL

include "juce/juce_graphics/colour/juce_Colour.pyx"
include "juce/juce_graphics/colour/juce_Colours.pyx"

include "echomesh/audio/DefaultDevice.pyx"
include "echomesh/audio/Loudness.pyx"
include "echomesh/audio/RingBuffer.pyx"
include "echomesh/audio/RingBufferIndex.pyx"
include "echomesh/audio/Source.pyx"
include "echomesh/base/Echomesh.pyx"
include "echomesh/color/Recolumn.pyx"
include "echomesh/color/Color.pyx"
include "echomesh/color/ColorList.pyx"
include "echomesh/color/ColorSpread.pyx"
include "echomesh/color/Concatenate.pyx"
include "echomesh/color/Insert.pyx"
include "echomesh/color/Mirror.pyx"
include "echomesh/color/Rows.pyx"
include "echomesh/color/Transform.pyx"
include "echomesh/color/Scroll.pyx"
include "echomesh/color/SPI.pyx"
include "echomesh/color/Tile.pyx"
include "echomesh/component/LightingWindow.pyx"
include "echomesh/util/EchomeshApplication.pyx"
include "echomesh/util/Log.pyx"
