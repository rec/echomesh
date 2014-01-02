#ifndef __ECHOMESH_HSB__
#define __ECHOMESH_HSB__

#include "echomesh/color/FColor.h"
#include "echomesh/color/RGB.h"

namespace echomesh {
namespace color {

class HSB : public ColorModel {
 public:
  void scale(FColor* c, float f) const override { scaleHSB(c, f); }
  void combine(const FColor& f, FColor* t) const override { combineHSB(f, t); }

  string toName(const FColor& c) const override {
    return RGB::toNameRGB(toRgb(c));
  }

  bool fromName(const string& s, FColor* c) const override {
    FColor rgb;
    bool success = RGB::fromNameRGB(s, &rgb);
    if (success)
      *c = fromRgb(rgb);
    return success;
  }

  string modelName() const override { return "HSB"; }

  FColor toRgb(const FColor& color) const override;
  FColor fromRgb(const FColor& color) const override;

  FColor interpolate(
      const FColor& begin, const FColor& end, float ratio) const override {
    auto h0 = hue(begin), s0 = saturation(begin), b0 = brightness(begin),
        a0 = begin.alpha();
    auto h1 = hue(end), s1 = saturation(end), b1 = brightness(end),
        a1 = end.alpha();
    return FColor(
        interpolateHue(h0, h1, ratio),
        s0 + ratio * (s1 - s0),
        b0 + ratio * (b1 - b0),
        a0 + ratio * (a1 - a0));
  }

  static float interpolateHue(float x, float y, float r) {
    if (fabs(x - y) <= 0.5) {
      return x + (y - x) * r;
    }

    float res = (x < y) ? (1 + x) - r * (1 + x - y) : x + r * (1 + y - x);
    return res - floorf(res);
  }

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
    hue(*t) = interpolateHue(hue(f), hue(*t), 0.5);
    saturation(*t) = jmax(saturation(*t), saturation(f));
    brightness(*t) = jmax(brightness(*t), brightness(f));
    t->alpha() = jmax(t->alpha(), f.alpha());
  }
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_HSB__
