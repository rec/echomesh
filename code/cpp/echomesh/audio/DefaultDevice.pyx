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

def default_output_sample_rate():
  return defaultOutputSampleRate()
