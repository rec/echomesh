#ifndef __ECHOMESH_HSB__
#define __ECHOMESH_HSB__

#include "echomesh/color/FColor.h"
#include "echomesh/color/RGB.h"

namespace echomesh {
namespace color {

class HSB : public ColorModel {
  void scale(FColor* c, float f) const override { scaleHSB(c, f); }
  void combine(const FColor& f, FColor* t) const override { combineHSB(f, t); }

  string toName(const FColor& c) const override {
    return RGB::toNameRGB(toRGB(c));
  }

  bool fromName(const string& s, FColor* c) const override {
    FColor rgb;
    bool success = RGB::fromNameRGB(s, &rgb);
    if (success)
      *c = fromRGB(rgb);
    return success;
  }

  FColor toRGB(const FColor& color) const override;
  FColor fromRGB(const FColor& color) const override;

  static const float& hue(const FColor& c) { return c.parts()[0]; }
  static const float& saturation(const FColor& c) { return c.parts()[1]; }
  static const float& brightness(const FColor& c) { return c.parts()[2]; }

  static float& hue(FColor& c) { return c.parts()[0]; }
  static float& saturation(FColor& c) { return c.parts()[1]; }
  static float& brightness(FColor& c) { return c.parts()[2]; }

  static void scaleHSB(FColor* c, float f) {
    brightness(*c) *= f;
  }

  static void combineHSB(const FColor& f, FColor* t) {
    auto h1 = hue(f), h2 = hue(*t), h3 = jmin(h1, h2), h4 = jmax(h1, h2);
    auto d1 = h4 - h3, d2 = (h3 + 1) - h4;

    if (d1 < d2) {
      hue(*t) = (h1 + h2) / 2;
    } else {
      auto a = (h3 + 1) / 2;
      hue(*t) = a - floor(a);
    }

    saturation(*t) = jmax(saturation(*t), saturation(f));
    brightness(*t) = jmax(brightness(*t), brightness(f));
  }

};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_HSB__
