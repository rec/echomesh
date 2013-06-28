#include "echomesh/base/Config.h"
#include "echomesh/audio/Envelope.h"

namespace echomesh {

static SampleRate SAMPLE_RATE(44100.0);

void operator>>(const Node& node, Envelope& env) {
  fillArray(node["data"], &env.data);
  node["loop_length"] >> env.loopLength;
  node["loops"] >> env.loops;
  node["reverse"] >> env.reverse;

  const Node& times = node["times"];
  env.times.resize(times.size());
  RealTime time;
  for (int i = 0; i < times.size(); ++i) {
    times[i] >> time;
    env.times[i] = SampleTime(time, SAMPLE_RATE);
  }
}

void operator>>(const Node& node, Value& value) {
  node["is_constant"] >> value.isConstant;
  if (value.isConstant)
    node["value"] >> value.value;
  else
    node["envelope"] >> value.envelope;
}

}  // namespace echomesh
