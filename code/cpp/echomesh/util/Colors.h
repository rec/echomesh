#ifndef __ECHOMESH_COLORS__
#define __ECHOMESH_COLORS__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

struct FColor {
  FColor() {}
  FColor(float red, float green, float blue, float alpha=1.0)
      : red_(red), green_(green), blue_(blue), alpha_(alpha) {
  }
  FColor(const Colour& c)
      : red_(c.getFloatRed()),
        green_(c.getFloatGreen()),
        blue_(c.getFloatBlue()),
        alpha_(c.getFloatAlpha()) {
  }

  float red_, green_, blue_, alpha_;

  operator Colour() const {
    return Colour::fromFloatRGBA(red_, green_, blue_, alpha_);
  }

  bool operator==(const FColor& other) const;

  static FColor NO_COLOR;
};

typedef vector<FColor> FColorList;

bool fillColor(const String& name, FColor* color);
FColor colorFromInt(uint32 argb);
string colorName(const FColor& color);
inline void copyColor(const FColor& from, FColor* to) { *to = from; }
void sortFColorList(FColorList*);
int compareColors(const FColor& x, const FColor& y);
int countColorsInList(const FColorList&, const FColor&);
int indexColorInList(const FColorList&, const FColor&);
void reverseFColorList(FColorList*);
void fillFColorList(
    FColorList*, const FColor& begin, const FColor& end, int size);
FColor interpolate(const FColor& begin, const FColor& end, int index, int size);

inline FColor makeFColor(float red, float green, float blue, float alpha) {
  return FColor(red, green, blue, alpha);
}

}  // namespace echomesh

#endif  // __ECHOMESH_COLORS__
