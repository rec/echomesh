#ifndef __ECHOMESH_COLORS__
#define __ECHOMESH_COLORS__

#include "rec/base/base.h"

namespace echomesh {

bool fillColor(const String& name, Colour* color);
Colour colorFromInt(uint32 argb);

}  // namespace echomesh

#endif  // __ECHOMESH_COLORS__
