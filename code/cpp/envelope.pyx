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
