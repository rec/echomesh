#include "echomesh/color/Mirror.h"

namespace echomesh {
namespace color {

FColorList mirror(
    const FColorList& fcl, int x, int y, bool reverseX, bool reverseY) {
  FColorList result;
  result.resize(fcl.size());
  for (auto i = 0; i < fcl.size(); ++i) {
    auto my_y = i / x;
    auto my_x = i - (my_y * x);
    if (reverseX)
      my_x = x - my_x - 1;
    if (reverseY)
      my_y = y - my_y - 1;
    auto index = my_x * y + my_y;
    if (index < fcl.size())
      result[index] = fcl[i];
  }
  return result;
}

}  // namespace color
}  // namespace echomesh
