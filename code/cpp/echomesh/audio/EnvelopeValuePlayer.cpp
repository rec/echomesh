#include "echomesh/audio/EnvelopeValuePlayer.h"

namespace echomesh {

EnvelopeValuePlayer::EnvelopeValuePlayer(const EnvelopeValue& ev)
    : envelopeValue_(ev), isConstant_(ev.isConstant) {
  if (not isConstant_ and points().size() < 2)
    throw Exception("Received an envelope with less than two points.");
}

void EnvelopeValuePlayer::begin() {
  loops_ = index_ = 0;

  float value = isConstant_ ? envelopeValue_.value : points()[0].value;
  point_ = Envelope::Point(0, value);
}

// The following statements are always true when getSegments begins or ends:
//
//   index_ < points().length - 1
//   point_.time < length_
//   point_.time >= envelope.points[index_].time
//   point_.time < envelope.points[index_ + 1].time

typedef EnvelopeValuePlayer::SegmentList SegmentList;

SegmentList EnvelopeValuePlayer::getSegments(SampleTime numSamples) {
  typedef Envelope::Point Point;

  SegmentList result;
  Segment seg;
  bool reverse = envelopeValue_.envelope.reverse;
  seg.first = Point(0, point_.value);
  if (loops_ > envelopeValue_.envelope.loops) {
    seg.second = Point(numSamples, point_.value);
    result.push_back(seg);
    numSamples = 0;
  }

  while (numSamples > 0) {
    const Point* previous = &points()[index_];
    const Point* next = previous + 1;

    bool forward = not (reverse and loops_ % 2);
    int directionMult = forward ? 1 : -1;
    SampleTime now = point_.time;
    SampleTime remains = forward ? (next->time - now) : (now - previous->time);

    if (remains <= numSamples) {
      // Move to a different index.
      if (forward) {
        if (++index_ >= points().size() - 1) {
          loops_++;
          if (not reverse)
            index_ = 0;
        }
      } else {
        if (--index_ < 0) {
          loops_++;
          if (not reverse)
            index_ = points().size() - 2;
        }
      }
    }

    Point delta = *next - *previous;
    float slope = directionMult * delta.value / delta.time;

    SampleTime t = jmin(remains, numSamples);
    numSamples -= t;
    point_.time += directionMult * t;

    seg.second = Point(seg.first.time + t, seg.first.value + slope * t);
    result.push_back(seg);
    seg.first = seg.second;
  }

  return result;
}

}  // namespace echomesh
