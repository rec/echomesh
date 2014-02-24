#pragma once

#include "echomesh/color/FColorList.h"

namespace echomesh {
namespace color {

FColorList scroll(const FColorList&, int dx, int dy, int xSize, bool wrap);

}  // namespace color
}  // namespace echomesh
