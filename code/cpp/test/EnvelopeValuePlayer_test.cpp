#include <gtest/gtest.h>
#include <istream>
#include <iostream>

#include "echomesh/audio/EnvelopeValuePlayer.h"
#include "yaml-cpp/yaml.h"

namespace echomesh {

namespace {

typedef Envelope::Point Point;
typedef EnvelopeValuePlayer::SegmentList SegmentList;

const float EPSILON = 0.000001;

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

  void assertPoint(int i, const Point& p, const Point& q) {
    ASSERT_NEAR(first(i).value, p.value, EPSILON);
    ASSERT_EQ(first(i).time, p.time);
    ASSERT_NEAR(second(i).value, q.value, EPSILON);
    ASSERT_EQ(second(i).time, q.time);
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

TEST_F(EnvelopeValuePlayerTest, TwoParts) {
  add(0, 0);
  add(1000, 1.0);
  begin();
  EXPECT_FALSE(player_->isConstant());
  EXPECT_EQ(player_->value(), 0.0);

  test(250);
  ASSERT_EQ(segments_.size(), 1);
  assertPoint(0, Point(0, 0.0), Point(250, 0.250));

  test(740);
  assertPoint(0, Point(0, 0.250), Point(740, 0.990));

  test(10);
  ASSERT_EQ(segments_.size(), 1);
  assertPoint(0, Point(0, 0.990), Point(10, 1.0));

  test(10);
  ASSERT_EQ(segments_.size(), 1);
  assertPoint(0, Point(0, 0.0), Point(10, 0.01));
}

TEST_F(EnvelopeValuePlayerTest, OverBoundary) {
  add(0, 0);
  add(1000, 1.0);
  begin();
  EXPECT_FALSE(player_->isConstant());
  EXPECT_EQ(player_->value(), 0.0);

  test(990);
  ASSERT_EQ(segments_.size(), 1);
  assertPoint(0, Point(0, 0.0), Point(990, 0.990));

  test(20);
  ASSERT_EQ(segments_.size(), 2);
  assertPoint(0, Point(0, 0.990), Point(10, 1.000));
  assertPoint(1, Point(10, 0.0), Point(20, 0.010));

  test(10);
  ASSERT_EQ(segments_.size(), 1);
  assertPoint(0, Point(0, 0.010), Point(10, 0.020));
}

TEST_F(EnvelopeValuePlayerTest, ThreeParts) {
  add(0, 0);
  add(1000, 1.0);
  add(1500, 2.0);
  begin();
  EXPECT_FALSE(player_->isConstant());
  EXPECT_EQ(player_->value(), 0.0);

  test(990);
  ASSERT_EQ(segments_.size(), 1);
  assertPoint(0, Point(0, 0.0), Point(990, 0.990));

  test(20);
  ASSERT_EQ(segments_.size(), 2);
  assertPoint(0, Point(0, 0.990), Point(10, 1.000));
  assertPoint(1, Point(10, 1.000), Point(20, 1.020));

  test(10);
  ASSERT_EQ(segments_.size(), 1);
  assertPoint(0, Point(0, 1.020), Point(10, 1.040));

  test(500);
  ASSERT_EQ(segments_.size(), 2);
  assertPoint(0, Point(0, 1.040), Point(480, 2.000));
  assertPoint(1, Point(480, 0.0), Point(500, 0.020));
}

TEST_F(EnvelopeValuePlayerTest, Loops) {
  add(0, 0);
  add(1000, 1.0);
  add(1500, 2.0);
  envelopeValue_.envelope.loops = 2;

  begin();
  test(4000);
  ASSERT_EQ(segments_.size(), 5);
}

}  // namespace echomesh
