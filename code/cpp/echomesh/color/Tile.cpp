#include "echomesh/color/Tile.h"
#include "echomesh/color/Rows.h"

namespace echomesh {
namespace color {

FColorList tile(const FColorList& fcl, int xMult, int yMult, int columns) {
  FColorList result;
  auto rows = computeRows(fcl.size(), columns);
  auto newColumns = columns * xMult;
  auto newRows = rows * yMult;
  result.resize(newColumns * newRows);

  for (auto my = 0; my < yMult; ++my) {
    for (auto mx = 0; mx < xMult; ++mx) {
      for (auto y = 0; y < rows; ++y) {
        for (auto x = 0; x < columns; ++x) {
          auto index = x + mx * columns + newColumns * (y + my * rows);
          result[index] = fcl[x + y * rows];
        }
      }
    }
  }

  return result;
}

}  // namespace color
}  // namespace echomesh
