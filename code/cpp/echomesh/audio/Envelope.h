#ifndef __ECHOMESH_ENVELOPE__
#define __ECHOMESH_ENVELOPE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

struct Envelope {
  struct Point {
    Point() {}
    Point(SampleTime t, float v) : time(t), value(v) {}

    SampleTime time;
    float value;
    String toString() const { return String(time) + "=" + String(value); }
  };

  typedef vector<Point> PointList;

  SampleTime length;
  int loops;
  PointList points;
  bool reverse;
};

inline Envelope::Point operator-(const Envelope::Point& x,
                                 const Envelope::Point& y) {
  return Envelope::Point(x.time - y.time, x.value - y.value);
}


// Normalize an envelope so that the first segment always starts at zero,
// and the last segment always is at least as long as length.
void normalizeEnvelope(Envelope*);

struct EnvelopeValue {
  bool isConstant;
  Envelope envelope;
  float value;
};

struct Playback {
  SampleTime begin, end;
  string filename;
  rec::SampleTime length;
  EnvelopeValue level;
  int loops;
  EnvelopeValue pan;
  bool passthrough;
};

void operator>>(const Node&, Envelope&);
void operator>>(const Node&, EnvelopeValue&);
void operator>>(const Node&, Playback&);

}  // namespace echomesh

#endif  // __ECHOMESH_ENVELOPE__
