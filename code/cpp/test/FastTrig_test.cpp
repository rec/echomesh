#include <math.h>
// #include <istream>
// #include <iostream>

#include <gtest/gtest.h>

#include "echomesh/util/FastTrig.h"
#include "yaml-cpp/yaml.h"

namespace echomesh {

namespace {

const float EPSILON = 0.002;
const float PI = M_PI;
const float PI2 = M_PI / 2.0;
const int PARTS = 256;

}  // namespace

#define EXPECT_TRIG(x) \
  EXPECT_NEAR(fastSin(x), sin(x), EPSILON); \
  EXPECT_NEAR(fastCos(x), cos(x), EPSILON)


TEST(FastTrig, Basic) {
  EXPECT_TRIG(0);
  EXPECT_TRIG(PI2);

  for (int i = 0; i < PARTS; ++i) {
    EXPECT_TRIG((i * PI2) / PARTS);
  }
}

}  // namespace echomesh
