# distutils: language = c++

from libcpp cimport bool
from libcpp.vector cimport vector

cdef extern from "rec/base/SampleTime.h" namespace "rec":
  cdef cppclass SampleTime:
    SampleTime(long long)
    long long get()


cdef extern from "echomesh/audio/Envelope.h" namespace "echomesh::audio":
  cdef struct EnvelopePoint:
    SampleTime time
    float value

  ctypedef vector[EnvelopePoint] EnvelopePointList

  cdef struct Envelope:
    SampleTime length
    int loops
    EnvelopePointList points
    bool reverse
    bool isConstant
    float value

  cdef void normalizeEnvelope(Envelope*)
  cdef Envelope* newEnvelope()
  cdef void deleteEnvelope(Envelope*)

cdef class PyEnvelope:
  cdef Envelope* thisptr
  def __cinit__(self, env):
    self.thisptr = newEnvelope()  # new Envelope()
    is_constant = env.is_constant()
    self.thisptr.isConstant = is_constant
    if is_constant:
      self.thisptr.value = env.value

  def __dealloc__(self):
    deleteEnvelope(self.thisptr)  # del self.thisptr

