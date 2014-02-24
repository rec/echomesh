#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {

template <typename Number>
bool isNegative(Number n) { return n < 0; }

inline bool isNegative(unsigned char) { return false; }
inline bool isNegative(unsigned short) { return false; }
inline bool isNegative(unsigned int) { return false; }
inline bool isNegative(unsigned long) { return false; }
inline bool isNegative(unsigned long long) { return false; }

template <typename Number>
Number abs(Number x) { return isNegative(x) ? -x : x; }

template <typename X, typename Y>
auto mod(X dividend, Y divisor) -> decltype(dividend % divisor) {
  auto modulo = dividend % divisor;
  if (isNegative(modulo))
    modulo += abs(divisor);
  return modulo;
}


}  // namespace echomesh
