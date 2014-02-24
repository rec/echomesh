#include "echomesh/color/Scroll.h"
#include "echomesh/color/ColorName.h"
#include "echomesh/util/Math.h"

namespace echomesh {
namespace color {

FColorList scroll(const FColorList& fcl, int dx, int dy, int xSize, bool wrap) {
  int size = fcl.size();
  auto ySize = size / xSize;

  if (size % xSize)
    ySize++;

  FColorList result;
  result.resize(xSize * ySize);

  if (not wrap and (abs(dx) >= xSize or abs(dy) >= ySize)) {
    result.setAll(FColor::BLACK);
  } else {
    for (auto y = 0; y < ySize; ++y) {
      for (auto x = 0; x < xSize; ++x) {
        auto& r = result[x + y * xSize];

        auto x2 = x - dx, y2 = y - dy;
        auto x3 = mod(x2, xSize), y3 = mod(y2, ySize);
        if (not wrap and (x2 != x3 or y2 != y3)) {
          r = FColor::BLACK;
        } else {
          auto i = x3 + y3 * xSize;
          r = (i < fcl.size()) ? fcl[i] : FColor::BLACK;
        }
        if (false)
        LOG(INFO)
            << "x: "
            << x2 << ", "
            << x3
            << ",  y: "
            << y2 << ", "
            << y3 << ", "
            << rgbToName(r);
      }
    }
  }

  return result;
}

}  // namespace color
}  // namespace echomesh
