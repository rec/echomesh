#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

inline int computeRows(int size, int columns) {
    return size / columns + ((size % columns) ? 1 : 0);
}

}  // namespace color
}  // namespace echomesh
