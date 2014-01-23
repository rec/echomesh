#pragma once

#include "echomesh/color/FColorList.h"

namespace echomesh {
namespace color {

FColorList insert(const FColorList& fcl,
                  int offset, uint length, bool rollover, int skip);

}  // namespace color
}  // namespace echomesh
