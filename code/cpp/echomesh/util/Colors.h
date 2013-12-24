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
int compareColors(Colour x, Colour y);
int countColorsInList(const ColourList&, Colour);
int indexColorInList(const ColourList&, Colour);
void reverseColorList(ColorList*);

}  // namespace echomesh

#endif  // __ECHOMESH_COLORS__
