#ifndef __ECHOMESH_COLORS__
#define __ECHOMESH_COLORS__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

bool fillColor(const String& name, Colour* color);
Colour colorFromInt(uint32 argb);
string colorName(const Colour& color);
inline void copyColor(const Colour& from, Colour* to) { *to = from; }

}  // namespace echomesh

#endif  // __ECHOMESH_COLORS__
