#include "echomesh/base/Config.h"
#include "echomesh/audio/Envelope.h"

namespace echomesh {

void operator>>(const Node& node, Envelope& env) {
  fillArray(node["data"], &env.data);
  node["length"] >> env.length;
  node["loops"] >> env.loops;
  node["reverse"] >> env.reverse;
  fillArray(node["times"], &env.times);
}

void operator>>(const Node& node, Value& value) {
  node["is_constant"] >> value.isConstant;
  if (value.isConstant)
    node["value"] >> value.value;
  else
    node["envelope"] >> value.envelope;
}

void operator>>(const Node& node, Playback& playback) {
  node["begin"] >> playback.begin;
  node["end"] >> playback.end;
  node["file"] >> playback.file;
  node["length"] >> playback.length;
  node["level"] >> playback.level;
  node["loops"] >> playback.loops;
  node["pan"] >> playback.pan;
  node["passthrough"] >> playback.passthrough;
}

}  // namespace echomesh
