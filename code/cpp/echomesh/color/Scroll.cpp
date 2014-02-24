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
      }
    }
  }

  return result;
}

FColorList smoothScroll(const FColorList& fcl, float dx, float dy, int xSize,
                        bool wrap) {
  auto dx1 = static_cast<int>(dx), dy1 = static_cast<int>(dy);
  auto xSame = near(dx1, dx), ySame = near(dy1, dy);

  if (xSame and ySame)
    return scroll(fcl, dx1, dy1, xSize, wrap);

  int dx2 = dx1 + (xSame ? 0 : (dx > 0 ? 1 : -1));
  int dy2 = dy1 + (ySame ? 0 : (dy > 0 ? 1 : -1));

  float rx = (dx > 0) ? (dx - dx1) : (dx1 - dx);
  float ry = (dy > 0) ? (dy - dy1) : (dy1 - dy);

  auto rxZero = near(rx, 0.0f), ryZero = near(ry, 0.0f);

  DCHECK(not (rxZero and ryZero));

  FColorList fcl1 = scroll(fcl, dx1, dy1, xSize, wrap);
  FColorList fcl2 = scroll(fcl, dx2, dy2, xSize, wrap);

  auto r = rxZero ? ry : (ryZero ? rx : (rx + ry) / 2.0f);
  return fcl1.interpolate(fcl2, r);
}

}  // namespace color
}  // namespace echomesh
