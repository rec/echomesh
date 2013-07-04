#include <gtest/gtest.h>

#include "echomesh/audio/EnvelopeValuePlayer.h"

namespace echomesh {

TEST(EnvelopeValuePlayer, Base) {
  EnvelopeValue ev;
  ev.isConstant = true;
  ev.value = 23.0;

  EnvelopeValuePlayer player(ev);
  ASSERT_TRUE(player.isConstant());
}

}  // namespace echomesh
