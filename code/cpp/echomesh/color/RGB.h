#ifndef __ECHOMESH_RGB__
#define __ECHOMESH_RGB__

#include "echomesh/color/FColor.h"
#include "echomesh/color/ColorModel.h"
#include "echomesh/color/ColorName.h"

namespace echomesh {
namespace color {

class RGB : public ColorModel {
 public:
  void scale(FColor* c, float s) const override { scaleRGB(c, s); }
  void combine(const FColor& x, FColor* y) const override { combineRGB(x, y); }

  string toName(const FColor& c) const override {
    return toNameRGB(c);
  }

  bool fromName(const string& s, FColor* c) const override {
    return fromNameRGB(s, c);
  }

  FColor toRgb(const FColor& color) const override {
    return color;
  }

  FColor fromRgb(const FColor& color) const override {
    return color;
  }

  string modelName() const override { return "rgb"; }

  bool isRgb() const override { return true; }

  FColor interpolate(
      const FColor& begin, const FColor& end, float ratio) const override {
    auto r0 = red(begin), g0 = green(begin), b0 = blue(begin), a0 = begin.alpha();
    auto r1 = red(end), g1 = green(end), b1 = blue(end), a1 = end.alpha();
    return FColor(
        r0 + ratio * (r1 - r0),
        g0 + ratio * (g1 - g0),
        b0 + ratio * (b1 - b0),
        a0 + ratio * (a1 - a0));
  }

  static const float& red(const FColor& fc) { return fc.red(); }
  static const float& green(const FColor& fc) { return fc.green(); }
  static const float& blue(const FColor& fc) { return fc.blue(); }

  static float& red(FColor& fc) { return fc.red(); }
  static float& green(FColor& fc) { return fc.green(); }
  static float& blue(FColor& fc) { return fc.blue(); }

  static Colour toColour(const FColor& fc) {
    return Colour(floatToUInt8(red(fc)),
                  floatToUInt8(green(fc)),
                  floatToUInt8(blue(fc)),
                  floatToUInt8(fc.alpha()));
  }

  static FColor fromColour(const Colour& c) {
    return FColor(c.getFloatRed(), c.getFloatGreen(), c.getFloatBlue(),
                  c.getFloatAlpha());
  }

  static void combineRGB(const FColor& x, FColor* y) {
    red(*y) = std::max(red(*y), red(x));
    green(*y) = std::max(green(*y), green(x));
    blue(*y) = std::max(blue(*y), blue(x));
    y->alpha() = std::max(y->alpha(), x.alpha());
  }

  static void scaleRGB(FColor* color, float scale) {
    red(*color) *= scale;
    green(*color) *= scale;
    blue(*color) *= scale;
  }

  static string toNameRGB(const FColor& c) {
    return rgbToName(c);
  }

  static bool fromNameRGB(const string& s, FColor* c) {
    return nameToRgb(s, c);
  }

  static uint8 floatToUInt8(const float n) {
    return static_cast<uint8>(jmax(0.0f, jmin(255.0f, n * 255.1f)));
  }
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_RGB__
