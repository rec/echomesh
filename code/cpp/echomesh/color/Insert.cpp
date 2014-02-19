#include "echomesh/color/Insert.h"

namespace echomesh {
namespace color {

static int mod(int dividend, int divisor) {
  auto modulo = dividend % divisor;
  if (modulo < 0)
    modulo += abs(divisor);
  return modulo;
}

FColorList insert(const FColorList& fcl,
                  int offset, uint length, bool rollover, int skip) {
  FColorList result;
  result.resize(length);
  result.setAll(FColor::BLACK);
  for (auto& color: fcl) {
    result[mod(offset, length)] = color;
    offset += skip;
  }
  return result;
}

}  // namespace color
}  // namespace echomesh
