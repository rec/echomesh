#ifndef __ECHOMESH_COLORS__
#define __ECHOMESH_COLORS__

#include "echomesh/color/FColor.h"
#include "echomesh/color/RGB.h"

namespace echomesh {

inline void combineRgb(const FColor& x, FColor* y) { RGB::combine(x, y); }
inline Colour rgbToColour(const FColor& fc) { return RGB::toColour(fc); }
inline FColor colourToRgb(const Colour& c) { return RGB::fromColour(c); }
inline void scaleRgb(FColor* color, float s) { return RGB::scale(color, s); }

typedef vector<FColor> FColorList;

bool fillColor(const String& name, FColor* color);
string colorName(const FColor& color);
inline void copyColor(const FColor& from, FColor* to) { *to = from; }
void sortFColorList(FColorList*);
int compareColors(const FColor& x, const FColor& y);
int countColorsInList(const FColorList&, const FColor&);
int indexColorInList(const FColorList&, const FColor&);
void reverseFColorList(FColorList*);
void fillFColorList(
    FColorList*, const FColor& begin, const FColor& end, int size);

FColor interpolate(const FColor& begin, const FColor& end, float ratio);

inline FColor makeFColor(float red, float green, float blue, float alpha) {
  return FColor(red, green, blue, alpha);
}

inline void scaleFColorList(FColorList* fc, float scale) {
  for (auto& c: *fc)
    scaleRgb(&c, scale);
}

inline void combineFColorList(const FColorList& from, FColorList* to) {
  if (from.size() > to->size())
    to->resize(from.size());
  for (auto i = 0; i < from.size(); ++i)
    combineRgb(from[i], &(*to)[i]);
}

}  // namespace echomesh

#endif  // __ECHOMESH_COLORS__
