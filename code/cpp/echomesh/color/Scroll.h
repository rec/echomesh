#pragma once

#include "echomesh/color/FColorList.h"

namespace echomesh {
namespace color {

FColorList scroll(const FColorList&, int dx, int dy, int xSize, bool wrap);
FColorList smoothScroll(const FColorList&, float dx, float dy, int xSize,
                        bool wrap);

}  // namespace color
}  // namespace echomesh
