#include "echomesh/audio/Envelope.h"

namespace echomesh {
namespace audio {

void normalizeEnvelope(Envelope* envelope) {
    if (not envelope || envelope->points.empty())
        return;

    auto points = envelope->points;

    if (points.front().time > 0)
        points.insert(points.begin(), EnvelopePoint(0, points.front().value));

    if (points.back().time < envelope->length)
        points.push_back(EnvelopePoint(envelope->length, points.back().value));
    else if (not envelope->length)
        envelope->length = points.back().time;
}

}  // namespace audio
}  // namespace echomesh
