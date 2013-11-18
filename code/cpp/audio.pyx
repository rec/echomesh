# distutils: language = c++

from libcpp.string cimport string

cdef extern from "echomesh/audio/DefaultDevice.h" namespace "echomesh::audio":
  double defaultInputSampleRate()
  double defaultOutputSampleRate()
  string defaultOutputDevice()
  string defaultInputDevice()

def default_output_device():
  return defaultOutputDevice()

def default_input_device():
  return defaultInputDevice()



cdef class AudioPlayer:
  def __cinit__(self, player):
    pass

