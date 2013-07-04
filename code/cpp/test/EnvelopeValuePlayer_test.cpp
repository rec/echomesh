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
  void test(SampleTime t) {
    segments_ = player_->getSegments(t);
  }

  const Point& first(int i) { return segments_[i].first; }
  const Point& second(int i) { return segments_[i].second; }

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

  SegmentList segments_;
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

  test(250);
  ASSERT_EQ(segments_.size(), 1);
  EXPECT_NEAR(first(0).value, 0.0, EPSILON);
  EXPECT_NEAR(second(0).value, 0.250, EPSILON);
  EXPECT_EQ(first(0).time, 0);
  EXPECT_EQ(second(0).time, 250);

  test(740);
  ASSERT_EQ(segments_.size(), 1);
  EXPECT_NEAR(first(0).value, 0.250, EPSILON);
  EXPECT_NEAR(second(0).value, 0.990, EPSILON);
  EXPECT_EQ(first(0).time, 0);
  EXPECT_EQ(second(0).time, 740);

  test(10);
  ASSERT_EQ(segments_.size(), 1);
  EXPECT_NEAR(first(0).value, 0.990, EPSILON);
  EXPECT_NEAR(second(0).value, 1.0, EPSILON);
  EXPECT_EQ(first(0).time, 0);
  EXPECT_EQ(second(0).time, 10);

  test(10);
  ASSERT_EQ(segments_.size(), 1);
  EXPECT_NEAR(first(0).value, 0.0, EPSILON);
  EXPECT_NEAR(second(0).value, 0.010, EPSILON);
  EXPECT_EQ(first(0).time, 0);
  EXPECT_EQ(second(0).time, 10);
}

TEST_F(EnvelopeValuePlayerTest, OverBoundary) {
  add(0, 0);
  add(1000, 1.0);
  begin();
  EXPECT_FALSE(player_->isConstant());
  EXPECT_EQ(player_->value(), 0.0);

  test(990);
  ASSERT_EQ(segments_.size(), 1);
  EXPECT_NEAR(first(0).value, 0.0, EPSILON);
  EXPECT_NEAR(second(0).value, 0.990, EPSILON);
  EXPECT_EQ(first(0).time, 0);
  EXPECT_EQ(second(0).time, 990);

  test(20);
  ASSERT_EQ(segments_.size(), 2);

  EXPECT_NEAR(first(0).value, 0.990, EPSILON);
  EXPECT_NEAR(second(0).value, 1.000, EPSILON);
  EXPECT_EQ(first(0).time, 0);
  EXPECT_EQ(second(0).time, 10);

  EXPECT_NEAR(first(1).value, 0.0, EPSILON);
  EXPECT_NEAR(second(1).value, 0.010, EPSILON);
  EXPECT_EQ(first(1).time, 10);
  EXPECT_EQ(second(1).time, 20);
}

}  // namespace echomesh
