#include "echomesh/audio/EnvelopePlayer.h"

namespace echomesh {
namespace audio {

EnvelopePlayer::EnvelopePlayer(Envelope* ev)
    : envelope_(ev),
      loops_(envelope_->loops) {
  if (not isConstant() and points().size() < 2)
    throw Exception("Received an envelope with less than two points.");
}


void EnvelopePlayer::jumpTo(SampleTime time) {
  // TODO
}

void EnvelopePlayer::begin() {
  loopCount_ = segmentIndex_ = 0;

  float v = isConstant() ? envelope_->value : points().front().value;
  point_ = EnvelopePoint(0, v);
}

// The following conditions are always true between calls to getSegments:
//
//   segmentIndex_ < points().length - 1
//   point_.time < length_
//   point_.time >= envelope.points[segmentIndex_].time
//   point_.time < envelope.points[segmentIndex_ + 1].time

typedef EnvelopePlayer::SegmentList SegmentList;

SegmentList EnvelopePlayer::getSegments(SampleTime numSamples) {
  SegmentList result;
  EnvelopePoint start(0, point_.value);
  Segment seg(start, start);
  bool reverse = envelope_->reverse;

  while (numSamples > 0) {
    if (loopsDone()) {
      seg.second = EnvelopePoint(seg.first.time + numSamples, point_.value);
      result.push_back(seg);
      break;
    }
    const EnvelopePoint* previous = &points()[segmentIndex_];
    const EnvelopePoint* next = previous + 1;

    bool forward = not (reverse and loopCount_ % 2);
    int directionMult = forward ? 1 : -1;
    SampleTime now = point_.time;
    SampleTime remains = forward ? (next->time - now) : (now - previous->time);

    bool rollover = false;
    if (remains <= numSamples) {
      // Move to a different index.
      if (forward) {
        if (++segmentIndex_ >= points().size() - 1) {
          loopCount_++;
          rollover = not (loopsDone() or reverse);
        }
      } else {
        if (--segmentIndex_ < 0) {
          loopCount_++;
        }
      }
    }

    EnvelopePoint delta = *next - *previous;
    float slope = delta.value / delta.time;

    SampleTime t = jmin(remains, numSamples);
    numSamples -= t;
    SampleTime dt = directionMult * t;
    float dv = slope * dt;
    point_.time += dt;
    point_.value += dv;

    seg.second.time += t;
    seg.second.value += dv;
    result.push_back(seg);

    if (rollover) {
      segmentIndex_ = 0;
      point_ = EnvelopePoint(0, points().front().value);
      seg.second.value = point_.value;
    }
    seg.first = seg.second;
  }

  return result;
}

}  // namespace audio
}  // namespace echomesh
