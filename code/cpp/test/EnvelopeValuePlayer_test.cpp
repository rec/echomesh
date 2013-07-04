#include <gtest/gtest.h>

#include "echomesh/audio/EnvelopeValuePlayer.h"

namespace echomesh {

namespace {

class EnvelopeValuePlayerTest : public ::testing::Test {
 public:
  EnvelopeValuePlayerTest() {}

 protected:
  void begin() {
    player_ = new EnvelopeValuePlayer(envelopeValue_);
    player_->begin();
  }

  EnvelopeValue envelopeValue_;
  ScopedPointer<EnvelopeValuePlayer> player_;
};

}  // namespace

TEST_F(EnvelopeValuePlayerTest, Base) {
  envelopeValue_.isConstant = true;
  envelopeValue_.value = 20.0;
  begin();
  ASSERT_TRUE(player_->isConstant());
  ASSERT_EQ(player_->value(), 20.0);
}

}  // namespace echomesh
