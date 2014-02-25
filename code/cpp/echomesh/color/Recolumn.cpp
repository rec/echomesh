#include "echomesh/color/Recolumn.h"
#include "echomesh/color/FColorList.h"
#include "echomesh/color/Rows.h"

namespace echomesh {
namespace color {

void recolumn(FColorList* fcl, int oldColumns, int newColumns) {
  if (oldColumns == newColumns or not (newColumns and oldColumns))
    return;

  auto rows = computeRows(fcl->size(), oldColumns);
  auto newSize = rows * newColumns;
  if (newColumns < oldColumns) {
    if (fcl->size() < newSize)
      fcl->resize(newSize);
    for (auto r = 1; r < rows; ++r) {
      auto oldOffset = r * oldColumns;
      auto newOffset = r * newColumns;
      for (auto c = 0; c < newColumns; ++c)
        fcl->set(fcl->get(oldOffset + c), newOffset + c);
    }
    fcl->resize(newSize);
  } else {
    fcl->resize(newSize);
    for (auto r = rows - 1; r > 0; --r) {
      auto oldOffset = r * oldColumns;
      auto newOffset = r * newColumns;
      for (auto c = oldColumns - 1; c >= 0; --c)
        fcl->set(fcl->get(oldOffset + c), newOffset + c);
      for (auto c = newColumns - 1; c >= oldColumns; --c)
        fcl->set(FColor::BLACK, newOffset + c);
    }
  }
}

}  // namespace color
}  // namespace echomesh
