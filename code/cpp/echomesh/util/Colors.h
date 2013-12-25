#ifndef __ECHOMESH_COLORS__
#define __ECHOMESH_COLORS__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

typedef vector<Colour> ColourList;

bool fillColor(const String& name, Colour* color);
Colour colorFromInt(uint32 argb);
string colorName(Colour color);
inline void copyColor(Colour from, Colour* to) { *to = from; }
void sortColourList(ColourList*);
int compareColors(Colour x, Colour y);
int countColorsInList(const ColourList&, Colour);
int indexColorInList(const ColourList&, Colour);
void reverseColourList(ColourList*);
void fillColourList(ColourList*, Colour begin, Colour end, int size);
Colour interpolate(Colour begin, Colour end, int index, int size);

}  // namespace echomesh

#endif  // __ECHOMESH_COLORS__
