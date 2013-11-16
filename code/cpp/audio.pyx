# distutils: language = c++

from libcpp.string cimport string

cdef extern from "echomesh/audio/DefaultDevice.h" namespace "echomesh::audio":
  double defaultInputSampleRate()
  double defaultOutputSampleRate()
  string defaultOutputDevice()
  string defaultInputDevice()

cdef extern from "JuceHeader.h" namespace "juce":
  cdef cppclass String:
    string toStdString()

cdef extern from "JuceHeader.h" namespace "juce::AudioDeviceManager":
  cdef struct AudioDeviceSetup:
    String outputDeviceName
    String inputDeviceName
    double sampleRate
    int bufferSize

def default_output_device():
  return defaultOutputDevice()

def default_input_device():
  return defaultInputDevice()

cdef class AudioPlayer:
  def __cinit__(self, player):
    pass

