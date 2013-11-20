#include "echomesh/base/Config.h"
#include "echomesh/audio/Envelope.h"

namespace echomesh {

void normalizeEnvelope(Envelope* envelope) {
  Envelope::PointList& points = envelope->points;
  if (points.front().time > 0)
    points.insert(points.begin(), Envelope::Point(0, points.front().value));

  if (points.back().time < envelope->length)
    points.push_back(Envelope::Point(envelope->length, points.back().value));
  else if (not envelope->length)
    envelope->length = points.back().time;
}

void operator>>(const Node& node, Envelope& env) {
  node["is_constant"] >> env.isConstant;
  if (env.isConstant) {
    node["value"] >> env.value;
    return;
  }

  const Node& subnode = node["envelope"];


  const Node& values = subnode["data"];
  const Node& times = subnode["times"];

  int size = jmin(values.size(), times.size());
  env.points.resize(size);

  for (int i = 0; i < size; ++i) {
    times[i] >> env.points[i].time;
    values[i] >> env.points[i].value;
  }

  subnode["length"] >> env.length;
  subnode["loops"] >> env.loops;
  subnode["reverse"] >> env.reverse;
  normalizeEnvelope(&env);
}

void operator>>(const Node& node, Playback& playback) {
  node["begin"] >> playback.begin;
  node["end"] >> playback.end;
  node["filename"] >> playback.filename;
  node["length"] >> playback.length;
  node["level"] >> playback.level;
  node["loops"] >> playback.loops;
  node["pan"] >> playback.pan;
  node["passthrough"] >> playback.passthrough;
}

}  // namespace echomesh
