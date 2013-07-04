#include <gtest/gtest.h>
#include <istream>
#include <iostream>

#include "echomesh/audio/EnvelopeValuePlayer.h"
#include "yaml-cpp/yaml.h"

namespace echomesh {

namespace {

typedef Envelope::Point Point;
typedef EnvelopeValuePlayer::SegmentList SegmentList;

class EnvelopeValuePlayerTest : public ::testing::Test {
 public:
  EnvelopeValuePlayerTest() : env_(&envelopeValue_.envelope) {
    envelopeValue_.isConstant = false;
    env_->loops = 0;
    env_->reverse = false;
    env_->length = 0;
  }

 protected:
  void set(const string& s) {
    std::istringstream iss(s);
    YAML::Parser parser(iss);
    YAML::Node node;
    parser.GetNextDocument(node);
    node >> envelopeValue_;
    begin();
  }

  void add(SampleTime time, float value) {
    env_->points.push_back(Point(time, value));
  }

  void begin() {
    if (not envelopeValue_.isConstant)
      normalizeEnvelope(env_);
    player_ = new EnvelopeValuePlayer(envelopeValue_);
    player_->begin();
  }

  EnvelopeValue envelopeValue_;
  Envelope* env_;
  ScopedPointer<EnvelopeValuePlayer> player_;
};

}  // namespace

TEST_F(EnvelopeValuePlayerTest, Constant) {
  envelopeValue_.isConstant = true;
  envelopeValue_.value = 20.0;
  begin();
  EXPECT_TRUE(player_->isConstant());
  EXPECT_EQ(player_->value(), 20.0);
}

static const float EPSILON = 0.000001;

TEST_F(EnvelopeValuePlayerTest, TwoParts) {
  add(0, 0);
  add(1000, 1.0);
  begin();
  EXPECT_FALSE(player_->isConstant());
  EXPECT_EQ(player_->value(), 0.0);

  SegmentList segments = player_->getSegments(250);
  ASSERT_EQ(segments.size(), 1);
  EXPECT_NEAR(segments[0].first.value, 0.0, EPSILON);
  EXPECT_NEAR(segments[0].second.value, 0.250, EPSILON);
  EXPECT_EQ(segments[0].first.time, 0);
  EXPECT_EQ(segments[0].second.time, 250);
}

}  // namespace echomesh
