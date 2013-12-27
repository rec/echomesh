#ifndef __ECHOMESH_RGB__
#define __ECHOMESH_RGB__

#include "echomesh/color/FColor.h"

namespace echomesh {

struct RGB {
  static const float& red(const FColor& fc) { return fc.x_; }
  static const float& green(const FColor& fc) { return fc.y_; }
  static const float& blue(const FColor& fc) { return fc.z_; }
  static float& red(FColor& fc) { return fc.x_; }
  static float& green(FColor& fc) { return fc.y_; }
  static float& blue(FColor& fc) { return fc.z_; }

  static void combine(const FColor& x, FColor* y) {
    y->red() = std::max(y->red(), x.red());
    y->green() = std::max(y->green(), x.green());
    y->blue() = std::max(y->blue(), x.blue());
    y->alpha() = std::max(y->alpha(), x.alpha());
  }

  static Colour toColour(const FColor& fc) {
    return Colour::fromFloatRGBA(fc.red(), fc.green(), fc.blue(), fc.alpha());
  }

  static FColor fromColour(const Colour& c) {
    return FColor(c.getFloatRed(), c.getFloatGreen(), c.getFloatBlue(),
                  c.getFloatAlpha());
  }

  static void scale(FColor* color, float scale) {
    color->red() *= scale;
    color->green() *= scale;
    color->blue() *= scale;
  }
};

}  // namespace echomesh

#endif  // __ECHOMESH_RGB__
