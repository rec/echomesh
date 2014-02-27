#include "echomesh/color/Insert.h"
#include "echomesh/util/math.h"

namespace echomesh {
namespace color {

FColorList insert(const FColorList& fcl,
                  int offset, uint length, bool rollover, int skip) {
  FColorList result;
  result.resize(length);
  for (auto& color: fcl) {
    result[mod(offset, length)] = color;
    offset += skip;
  }
  return result;
}

}  // namespace color
}  // namespace echomesh
