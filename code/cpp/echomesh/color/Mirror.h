#ifndef __ECHOMESH_COLOR_MIRROR__
#define __ECHOMESH_COLOR_MIRROR__

#include "echomesh/color/FColorList.h"

namespace echomesh {
namespace color {

FColorList mirror(
    const FColorList&, int x, int y, bool reverseX, bool reverseY);

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_COLOR_MIRROR__
