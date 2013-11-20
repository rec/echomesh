#ifndef __ECHOMESH_ENVELOPEVALUEPLAYER__
#define __ECHOMESH_ENVELOPEVALUEPLAYER__

#include "echomesh/audio/Envelope.h"

namespace echomesh {
namespace audio {

class EnvelopePlayer {
 public:
  typedef std::pair<Envelope::Point, Envelope::Point> Segment;
  typedef vector<Segment> SegmentList;

  EnvelopePlayer(const Envelope&);
  bool isConstant() const { return envelopeValue_.isConstant; }

  const Envelope::Point point() const { return point_; }
  float value() const { return point_.value; }
  const Envelope::PointList& points() const { return envelopeValue_.points; }

  void begin();
  void jumpTo(SampleTime);

  // Continue to play this envelope for "time", and return a list of segments
  // generated.  This is only legal to call if isConstant is false.
  SegmentList getSegments(SampleTime time);

 private:
  bool loopsDone() const { return loops_ and loopCount_ >= loops_; }

  const Envelope& envelopeValue_;
  const int loops_;

  Envelope::Point point_;
  int segmentIndex_;
  int loopCount_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(EnvelopePlayer);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_ENVELOPEVALUEPLAYER__
