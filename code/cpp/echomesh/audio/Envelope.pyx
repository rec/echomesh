include "rec/base/SampleTime.pyx"

from libcpp cimport bool
from libcpp.vector cimport vector


cdef extern from "echomesh/audio/Envelope.h" namespace "echomesh::audio":
  cdef cppclass EnvelopePoint:
    EnvelopePoint(SampleTime time, float value)
    SampleTime time
    float value

  ctypedef vector[EnvelopePoint] EnvelopePointList

  cdef cppclass Envelope:
    SampleTime length
    int loops
    EnvelopePointList points
    bool reverse
    bool isConstant
    float value

  cdef void normalizeEnvelope(Envelope*)
  cdef void addPoint(Envelope* env, long long time, float value)


cdef Envelope* makeEnvelope(env, sampleRate):
  if not env:
    return NULL
  newEnv = new Envelope()
  newEnv.isConstant = env['is_constant']

  if newEnv.isConstant:
    newEnv.value = env['value']
    newEnv.length = SampleTime(-1)
  else:
    ed = env['envelope']
    newEnv.length = SampleTime(sampleRate * ed['length'])
    newEnv.reverse = ed['reverse']
    newEnv.loops = ed['loops']
    for t, d in zip(ed['times'], ed['data']):
      addPoint(newEnv, sampleRate * t, d)
  normalizeEnvelope(newEnv)
  return newEnv
