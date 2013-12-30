#ifndef __ECHOMESH_COLORS__
#define __ECHOMESH_COLORS__

#include "echomesh/color/FColor.h"
#include "echomesh/color/FColorList.h"
#include "echomesh/color/RGB.h"

namespace echomesh {
namespace color {

inline FColor colourToRgb(const Colour& c) { return RGB::fromColour(c); }
inline Colour rgbToColour(const FColor& fc) { return RGB::toColour(fc); }

inline void scaleFColorList(FColorList* fc, float scale) {
  for (auto& c: *fc)
    RGB::scaleRGB(&c, scale);
}

inline void combineFColorList(const FColorList& from, FColorList* to) {
  if (from.size() > to->size())
    to->resize(from.size());
  for (auto i = 0; i < from.size(); ++i)
    RGB::combineRGB(from[i], &(*to)[i]);
}

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_COLORS__
