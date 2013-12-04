# distutils: language = c++

include "echomesh/util/AppCallback.pyx"
include "echomesh/audio/Envelope.pyx"

from libcpp.string cimport string

cdef extern from "echomesh/audio/Source.h" namespace "echomesh::audio":
  cdef cppclass Source:
    Source(string filename, int loops,
           double begin, double end, double length,
           string device, int channels, Envelope* gain, Envelope* pan,
           VoidCaller cb, void* callbackData, float sampleRate) except +
    void run()
    void begin()
    void pause()
    void unload()
    string error()

cdef class AudioSource:
  cdef Source *thisptr
  cdef object callback

  def __cinit__(self, string filename, int loops,
                double begin, double end, double length,
                string device, int channels, object gain, object pan,
                object callback, float sampleRate):
    self.callback = callback
    self.thisptr = new Source(filename, loops, begin, end, length,
                              device, channels,
                              makeEnvelope(gain, sampleRate),
                              makeEnvelope(pan, sampleRate),
                              perform_callback, <void*> callback,
                              sampleRate)
    error = self.thisptr.error()
    if self.thisptr.error().size():
      del self.thisptr
      self.thisptr = NULL
      raise Exception(error)

  def __dealloc__(self): self.unload()
  def run(self):    self.thisptr.run()
  def begin(self):  self.thisptr.begin()
  def pause(self):
    if self.thisptr:  # TODO: Pause should not be called after unload!
      self.thisptr.pause()

  def unload(self):
    t = self.thisptr
    del t
    self.thisptr = NULL
