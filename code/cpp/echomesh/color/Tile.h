#pragma once

#include "echomesh/color/FColorList.h"

namespace echomesh {
namespace color {

FColorList tile(const FColorList&, int xMult, int yMult, int columns);

FColorList tile_pieces(
    const FColorList&, int columns, int newColumns, int newRows,
    int xCenter, int yCenter);

}  // namespace color
}  // namespace echomesh
