#ifndef __ECHOMESH_ENVELOPEVALUEPLAYER__
#define __ECHOMESH_ENVELOPEVALUEPLAYER__

#include "echomesh/audio/Envelope.h"

namespace echomesh {
namespace audio {

class EnvelopePlayer {
 public:
  typedef std::pair<EnvelopePoint, EnvelopePoint> Segment;
  typedef vector<Segment> SegmentList;

  explicit EnvelopePlayer(Envelope*);
  bool isConstant() const { return envelope_->isConstant; }

  const EnvelopePoint point() const { return point_; }
  float value() const { return point_.value; }
  const EnvelopePointList& points() const { return envelope_->points; }

  void begin();
  void jumpTo(SampleTime);

  // Continue to play this envelope for "time", and return a list of segments
  // generated.  This is only legal to call if isConstant is false.
  SegmentList getSegments(SampleTime time);

 private:
  bool loopsDone() const { return loops_ and loopCount_ >= loops_; }

  unique_ptr<Envelope> envelope_;
  const int loops_;

  EnvelopePoint point_;
  int segmentIndex_;
  int loopCount_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(EnvelopePlayer);
};

}  // namespace audio
}  // namespace echomesh

#endif  // __ECHOMESH_ENVELOPEVALUEPLAYER__
