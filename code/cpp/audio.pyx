# distutils: language = c++

from libcpp.string cimport string

cdef extern from "echomesh/audio/Source.h" namespace "echomesh::audio":
  cdef cppclass Source:
    Source(string, int, long long, long long, long long, string, int) except +
    void run()
    void begin()
    void pause()
    void unload()

cdef class AudioSource:
  cdef Source *thisptr

  def __cinit__(self, string filename, int loops,
                long long begin, long long end, long long length,
                string device, int channels):
    self.thisptr = new Source(filename, loops, begin, end, length,
                              device, channels)

  def __dealloc__(self): del self.thisptr
  def run(self): self.thisptr.run()
  def begin(self): self.thisptr.begin()
  def pause(self): self.thisptr.pause()
  def unload(self): self.thisptr.unload()

cdef extern from "echomesh/audio/DefaultDevice.h" namespace "echomesh::audio":
  double defaultInputSampleRate()
  double defaultOutputSampleRate()
  string defaultOutputDevice()
  string defaultInputDevice()

def default_output_device():
  return defaultOutputDevice()

def default_input_device():
  return defaultInputDevice()

