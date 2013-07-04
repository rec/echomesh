#include <gtest/gtest.h>

#include "echomesh/audio/EnvelopeValuePlayer.h"

namespace echomesh {

namespace {

class EnvelopeValuePlayerTest : public ::testing::Test {
 public:
  EnvelopeValuePlayerTest() {}
  
 protected:
  void make() {
    player_ = new EnvelopeValuePlayer(ev_);
  }

  EnvelopeValue ev_;
  ScopedPointer<EnvelopeValuePlayer> player_;
};

}  // namespace

TEST_F(EnvelopeValuePlayerTest, Base) {
  make();
  ASSERT_TRUE(player_->isConstant());
}

}  // namespace echomesh
