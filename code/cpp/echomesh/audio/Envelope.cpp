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
  const Node& values = node["data"];
  const Node& times = node["times"];

  int size = jmin(values.size(), times.size());
  env.points.resize(size);

  for (int i = 0; i < size; ++i) {
    times[i] >> env.points[i].time;
    values[i] >> env.points[i].value;
  }

  node["length"] >> env.length;
  node["loops"] >> env.loops;
  node["reverse"] >> env.reverse;
  normalizeEnvelope(&env);
}

void operator>>(const Node& node, EnvelopeValue& value) {
  node["is_constant"] >> value.isConstant;
  if (value.isConstant)
    node["value"] >> value.value;
  else
    node["envelope"] >> value.envelope;
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
