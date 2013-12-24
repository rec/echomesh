#ifndef __ECHOMESH_COLORS__
#define __ECHOMESH_COLORS__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

typedef vector<Colour> ColourList;

bool fillColor(const String& name, Colour* color);
Colour colorFromInt(uint32 argb);
string colorName(Colour color);
inline void copyColor(Colour from, Colour* to) { *to = from; }
void sortColorList(ColourList*);
inline bool colorsEqual(Colour x, Colour y) { return x == y; }
int countColorsInList(const ColourList&, Colour);

}  // namespace echomesh

#endif  // __ECHOMESH_COLORS__
