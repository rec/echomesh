#include "echomesh/color/Scroll.h"
#include "echomesh/color/ColorName.h"
#include "echomesh/color/Rows.h"
#include "echomesh/color/Transform.h"
#include "echomesh/util/Math.h"

namespace echomesh {
namespace color {

FColorList scroll(
    const FColorList& fcl, int dx, int dy, int columns, bool wrap) {
    auto ySize = computeRows(fcl.size(), columns);
    FColorList result;

    if (dx or dy) {
        result.resize(columns * ySize);

        if (not wrap and (abs(dx) >= columns or abs(dy) >= ySize)) {
            result.setAll(FColor::BLACK);
        } else {
            for (auto y = 0; y < ySize; ++y) {
                for (auto x = 0; x < columns; ++x) {
                    auto x2 = x - dx, y2 = y - dy;
                    auto x3 = mod(x2, columns), y3 = mod(y2, ySize);
                    auto black = not wrap and (x2 != x3 or y2 != y3);
                    auto color = black ? FColor::BLACK : fcl.get(x3 + y3 * columns);
                    result.set(x + y * columns, color);
                }
            }
        }
    } else {
        result = fcl;
    }

    return result;
}

FColorList smoothScroll(
    const FColorList& fcl, float dx, float dy, int columns, bool wrap,
    const CTransform* transform) {
    auto dx1 = static_cast<int>(dx), dy1 = static_cast<int>(dy);
    auto xSame = near(dx1, dx), ySame = near(dy1, dy);

    if (xSame and ySame)
        return scroll(fcl, dx1, dy1, columns, wrap);

    int dx2 = dx1 + (xSame ? 0 : (dx > 0 ? 1 : -1));
    int dy2 = dy1 + (ySame ? 0 : (dy > 0 ? 1 : -1));

    float rx = (dx > 0) ? (dx - dx1) : (dx1 - dx);
    float ry = (dy > 0) ? (dy - dy1) : (dy1 - dy);

    auto rxZero = near(rx, 0.0f), ryZero = near(ry, 0.0f);

    DCHECK(not (rxZero and ryZero));

    FColorList fcl1 = scroll(fcl, dx1, dy1, columns, wrap);
    FColorList fcl2 = scroll(fcl, dx2, dy2, columns, wrap);

    auto r = rxZero ? ry : (ryZero ? rx : (rx + ry) / 2.0f);
    if (transform)
        r = transform->apply(r);
    return fcl1.interpolate(fcl2, r);
}

}  // namespace color
}  // namespace echomesh
