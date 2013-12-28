#ifndef __ECHOMESH_RGB__
#define __ECHOMESH_RGB__

#include "echomesh/color/FColor.h"

namespace echomesh {

struct RGB {
  static const float& red(const FColor& fc) { return fc.parts_[0]; }
  static const float& green(const FColor& fc) { return fc.parts_[1]; }
  static const float& blue(const FColor& fc) { return fc.parts_[2]; }

  static float& red(FColor& fc) { return fc.parts_[0]; }
  static float& green(FColor& fc) { return fc.parts_[1]; }
  static float& blue(FColor& fc) { return fc.parts_[2]; }

  static void combine(const FColor& x, FColor* y) {
    red(*y) = std::max(red(*y), red(x));
    green(*y) = std::max(green(*y), green(x));
    blue(*y) = std::max(blue(*y), blue(x));
    y->alpha() = std::max(y->alpha(), x.alpha());
  }

  static Colour toColour(const FColor& fc) {
    return Colour::fromFloatRGBA(red(fc), green(fc), blue(fc), fc.alpha());
  }

  static FColor fromColour(const Colour& c) {
    return FColor(c.getFloatRed(), c.getFloatGreen(), c.getFloatBlue(),
                  c.getFloatAlpha());
  }

  static void scale(FColor* color, float scale) {
    red(*color) *= scale;
    green(*color) *= scale;
    blue(*color) *= scale;
  }

  static FColor fromInt(uint32 argb) {
    return fromColour(Colour(argb));
  }

  static int compare(const FColor& x, const FColor& y) {
    if (red(x) < red(y))
      return -1;
    if (red(x) > red(y))
      return 1;
    if (green(x) < green(y))
      return -1;
    if (green(x) > green(y))
      return 1;
    if (blue(x) < blue(y))
      return -1;
    if (blue(x) > blue(y))
      return 1;
    if (x.alpha() < y.alpha())
      return -1;
    if (x.alpha() > y.alpha())
      return 1;
    return 0;
  }
};

}  // namespace echomesh

#endif  // __ECHOMESH_RGB__
