#pragma once

#include "echomesh/color/FColorList.h"

namespace echomesh {
namespace color {

class CTransform;

FColorList scroll(const FColorList&, int dx, int dy, int columns, bool wrap);
FColorList smoothScroll(const FColorList&, float dx, float dy, int columns,
                        bool wrap, const CTransform* transform = nullptr);

}  // namespace color
}  // namespace echomesh
