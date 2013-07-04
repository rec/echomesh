#ifndef __ECHOMESH_ENVELOPEVALUEPLAYER__
#define __ECHOMESH_ENVELOPEVALUEPLAYER__

#include "echomesh/audio/Envelope.h"

namespace echomesh {

class EnvelopeValuePlayer {
 public:
  typedef vector<Envelope::Point> PointList;

  EnvelopeValuePlayer(const EnvelopeValue&);
  bool isConstant() const { return envelopeValue_.isConstant; }

  const Envelope::Point point() const { return point_; }
  float value() const { return point_.value; }
  const Envelope::PointList& points() const {
    return envelopeValue_.envelope.points;
  }

  void begin();

  // Only call this if isConstant is false.
  PointList getSegments(SampleTime);

 private:
  const EnvelopeValue& envelopeValue_;
  const bool isConstant_;

  Envelope::Point point_;
  int index_;
  int loops_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(EnvelopeValuePlayer);
};

}  // namespace echomesh

#endif  // __ECHOMESH_ENVELOPEVALUEPLAYER__
