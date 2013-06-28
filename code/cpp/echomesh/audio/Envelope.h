#ifndef __ECHOMESH_ENVELOPE__
#define __ECHOMESH_ENVELOPE__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

struct Envelope {
  vector<double> data;
  rec::SampleTime loopLength;
  int loops;
  bool reverse;
  vector<SampleTime> times;

};

struct Value {
  bool isConstant;
  Envelope envelope;
  double value;
};

void operator>>(const Node&, Envelope&);
void operator>>(const Node&, Value&);

}  // namespace echomesh

#endif  // __ECHOMESH_ENVELOPE__
