#include "echomesh/audio/EnvelopeValuePlayer.h"

namespace echomesh {

EnvelopeValuePlayer::EnvelopeValuePlayer(const EnvelopeValue& ev)
    : envelopeValue_(ev),
      isConstant_(ev.isConstant),
      loops_(envelopeValue_.envelope.loops) {
  if (not isConstant_ and points().size() < 2)
    throw Exception("Received an envelope with less than two points.");
}

void EnvelopeValuePlayer::begin() {
  loopCount_ = index_ = 0;

  float value = isConstant_ ? envelopeValue_.value : points().front().value;
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
  Point start(0, point_.value);
  Segment seg(start, start);
  bool reverse = envelopeValue_.envelope.reverse;

  while (numSamples > 0) {
    if (loopsDone()) {
      seg.second = Point(seg.first.time + numSamples, point_.value);
      result.push_back(seg);
      break;
    }
    const Point* previous = &points()[index_];
    const Point* next = previous + 1;

    bool forward = not (reverse and loopCount_ % 2);
    int directionMult = forward ? 1 : -1;
    SampleTime now = point_.time;
    SampleTime remains = forward ? (next->time - now) : (now - previous->time);

    bool rollover = false;
    if (remains <= numSamples) {
      // Move to a different index.
      if (forward) {
        if (++index_ >= points().size() - 1) {
          loopCount_++;
          rollover = not (loopsDone() or reverse);
        }
      } else {
        if (--index_ < 0) {
          loopCount_++;
        }
      }
    }

    Point delta = *next - *previous;
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
      index_ = 0;
      point_ = Point(0, points().front().value);
      seg.second.value = point_.value;
    }
    seg.first = seg.second;
  }

  return result;
}

}  // namespace echomesh
