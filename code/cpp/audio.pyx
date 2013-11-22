# distutils: language = c++

include "envelope.pyx"

from libcpp.string cimport string

cdef extern from "echomesh/audio/Source.h" namespace "echomesh::audio":
  cdef cppclass Source:
    Source(string filename, int loops,
           long long begin, long long end, long long length,
           string device, int channels, Envelope* gain, Envelope* pan,
           Callback cb, void* callbackData) except +
    void run()
    void begin()
    void pause()
    void unload()
    string error()

cdef class AudioSource:
  cdef Source *thisptr

  def __cinit__(self, string filename, int loops,
                long long begin, long long end, long long length,
                string device, int channels, object gain, object pan,
                object pause):
    self.thisptr = new Source(filename, loops, begin, end, length,
                              device, channels,
                              makeEnvelope(gain), makeEnvelope(pan),
                              perform_callback, <void*> pause)
    error = self.thisptr.error()
    if self.thisptr.error().size():
      del self.thisptr
      self.thisptr = NULL
      raise Exception(error)

  def __dealloc__(self):
    print('deallocating')
    del self.thisptr
  def run(self):          self.thisptr.run()
  def begin(self):        self.thisptr.begin()
  def pause(self):        self.thisptr.pause()
  def unload(self):       self.thisptr.unload()

cdef extern from "echomesh/audio/DefaultDevice.h" namespace "echomesh::audio":
  double defaultInputSampleRate()
  double defaultOutputSampleRate()
  string defaultOutputDevice()
  string defaultInputDevice()
  string test1()
  string test2()

def default_output_device():
  return defaultOutputDevice()

def default_input_device():
  return defaultInputDevice()

def default_output_sample_rate():
  return defaultOutputSampleRate()
