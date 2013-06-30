#ifndef __ECHOMESH_ENVELOPE__
#define __ECHOMESH_ENVELOPE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

struct Envelope {
  vector<double> data;
  rec::SampleTime length;
  int loops;
  bool reverse;
  vector<SampleTime> times;
};

struct Value {
  bool isConstant;
  Envelope envelope;
  double value;
};

struct Playback {
  SampleTime begin, end;
  string file;
  Value level;
  int loops;
  Value pan;
  bool passthrough;
};

void operator>>(const Node&, Envelope&);
void operator>>(const Node&, Value&);
void operator>>(const Node&, Playback&);

}  // namespace echomesh

#endif  // __ECHOMESH_ENVELOPE__
