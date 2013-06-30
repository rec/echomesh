#include "echomesh/base/Config.h"
#include "echomesh/audio/Envelope.h"

namespace echomesh {

static SampleRate SAMPLE_RATE(44100.0);

void operator>>(const Node& node, Envelope& env) {
  RealTime time;
  node["begin"] >> time;
  env.begin = SampleTime(time, SAMPLE_RATE);

  node["end"] >> time;
  env.end = SampleTime(time, SAMPLE_RATE);

  fillArray(node["data"], &env.data);
  node["length"] >> env.length;
  node["loops"] >> env.loops;
  node["reverse"] >> env.reverse;

  const Node& times = node["times"];
  env.times.resize(times.size());
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

void operator>>(const Node& node, Playback& playback) {
  node["file"] >> playback.file;
  node["level"] >> playback.level;
  node["loops"] >> playback.loops;
  node["pan"] >> playback.pan;
  node["passthrough"] >> playback.passthrough;
}

}  // namespace echomesh
