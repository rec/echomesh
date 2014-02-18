#ifndef __ECHOMESH_ENVELOPE__
#define __ECHOMESH_ENVELOPE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

struct EnvelopePoint {
  EnvelopePoint() {}
  EnvelopePoint(SampleTime t, float v) : time(t), value(v) {}

  SampleTime time;
  float value;
};

inline EnvelopePoint subtract(
    const EnvelopePoint& x, const EnvelopePoint& y) {
  return EnvelopePoint(x.time - y.time, x.value - y.value);
}

typedef vector<EnvelopePoint> EnvelopePointList;

struct Envelope {
  SampleTime length;
  int loops;
  EnvelopePointList points;
  bool reverse;
  bool isConstant;
  float value;
};

inline void addPoint(Envelope* env, long long time, float value) {
  env->points.push_back(EnvelopePoint(time, value));
}

// Normalize an envelope so that the first segment always starts at zero,
// and the last segment always is at least as long as length.
void normalizeEnvelope(Envelope*);

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_ENVELOPE__
