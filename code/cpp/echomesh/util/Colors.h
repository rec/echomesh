#ifndef __ECHOMESH_COLORS__
#define __ECHOMESH_COLORS__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

struct RGB;
struct HSV;

struct FColor {
  FColor() {}
  FColor(float red, float green, float blue, float alpha=1.0)
      : x_(red), y_(green), z_(blue), alpha_(alpha) {
  }

  const float& alpha() const { return alpha_; }
  float& alpha() { return alpha_; }

  const float& red() const { return x_; }
  const float& green() const { return y_; }
  const float& blue() const { return z_; }

  float& red() { return x_; }
  float& green() { return y_; }
  float& blue() { return z_; }

  const float& hue() const { return x_; }
  const float& saturation() const { return y_; }
  const float& brightness() const { return z_; }

  float& hue() { return x_; }
  float& saturation() { return y_; }
  float& brightness() { return z_; }

  bool operator==(const FColor& other) const;

  static FColor NO_COLOR;

  FColor toHSB() const;
  FColor fromHSB() const;
  FColor toYIQ() const;
  FColor fromYIQ() const;

 private:
  float x_, y_, z_, alpha_;

  friend struct RGB;
  friend struct HSB;
};

struct RGB {
  void combineRgb(const FColor& x, FColor* y) {
    y->red() = std::max(y->red(), x.red());
    y->green() = std::max(y->green(), x.green());
    y->blue() = std::max(y->blue(), x.blue());
    y->alpha() = std::max(y->alpha(), x.alpha());
  }
};

static void combineRgb(const FColor& x, FColor* y) {
  y->red() = std::max(y->red(), x.red());
  y->green() = std::max(y->green(), x.green());
  y->blue() = std::max(y->blue(), x.blue());
  y->alpha() = std::max(y->alpha(), x.alpha());
}

inline Colour rgbToColour(const FColor& fc) {
  return Colour::fromFloatRGBA(fc.red(), fc.green(), fc.blue(), fc.alpha());
}

inline FColor colourToRgb(const Colour& c) {
  return FColor(c.getFloatRed(), c.getFloatGreen(), c.getFloatBlue(),
                c.getFloatAlpha());
}

inline void scaleRgb(FColor* color, float scale) {
  color->red() *= scale;
  color->green() *= scale;
  color->blue() *= scale;
}

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
