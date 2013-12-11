#include "echomesh/util/FastTrig.h"

namespace echomesh {

namespace {
float complement(float x) {
  return sqrtf(1.0 - x * x);
}

}

// From http://stackoverflow.com/questions/6091837/sin-and-cos-are-slow-is-there-an-alternatve

float fastSin(float theta) {
  auto B = 4.0f / M_PI;
  auto C = -4.0f / (M_PI*M_PI);
  auto P = 0.225f;

  auto y = (B  + C * theta) * theta;
  return P * (y * std::abs(y) - y) + y;
}

float fastCos(float theta) {
  return complement(fastSin(theta));
}

std::pair<float, float> fastSinCos(float theta) {
  auto s = fastSin(theta);
  return std::make_pair(s, complement(s));
}

}  // namespace echomesh

