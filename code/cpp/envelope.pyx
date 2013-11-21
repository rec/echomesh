# distutils: language = c++

from libcpp cimport bool
from libcpp.vector cimport vector

cdef extern from "rec/base/SampleTime.h" namespace "rec":
  cdef cppclass SampleTime:
    SampleTime(long long)
    long long get()


cdef extern from "echomesh/audio/Envelope.h" namespace "echomesh::audio":
  cdef struct EnvelopePoint:
    EnvelopePoint(SampleTime time, float value)
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
  cdef void addPoint(Envelope* env, long long time, float value)


cdef Envelope* makeEnvelope(env):
  newEnv = newEnvelope()  # new Envelope()
  newEnv.isConstant = env.is_constant
  newEnv.length = SampleTime(env.length)
  if newEnv.isConstant:
    newEnv.value = env.value
  else:
    newEnv.reverse = env.reverse
    newEnv.loops = env.loops
    for t, d in zip(env.times, env.data):
      addPoint(newEnv, t, d)
  normalizeEnvelope(newEnv)
  return newEnv
