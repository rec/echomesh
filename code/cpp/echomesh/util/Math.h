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

template <typename Number>
Number absoluteDifference(Number x, Number y) {
    return (x > y) ? (x - y) : (y - x);
}

template <typename Number>
bool near(Number x, Number y, Number diff) {
    return absoluteDifference(x, y) <= diff;
}

template <typename Number>
bool near(Number x, Number y) {
    return near(x, y, Number(0.000001));
}

}  // namespace echomesh
