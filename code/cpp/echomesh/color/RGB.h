#ifndef __ECHOMESH_RGB__
#define __ECHOMESH_RGB__

#include "echomesh/color/FColor.h"

namespace echomesh {
namespace color {

class RGB {
 public:
  static const float& red(const FColor& fc) { return fc.parts()[0]; }
  static const float& green(const FColor& fc) { return fc.parts()[1]; }
  static const float& blue(const FColor& fc) { return fc.parts()[2]; }

  static float& red(FColor& fc) { return fc.parts()[0]; }
  static float& green(FColor& fc) { return fc.parts()[1]; }
  static float& blue(FColor& fc) { return fc.parts()[2]; }

  static void combine(const FColor& x, FColor* y) {
    red(*y) = std::max(red(*y), red(x));
    green(*y) = std::max(green(*y), green(x));
    blue(*y) = std::max(blue(*y), blue(x));
    y->alpha() = std::max(y->alpha(), x.alpha());
  }

  static void scale(FColor* color, float scale) {
    red(*color) *= scale;
    green(*color) *= scale;
    blue(*color) *= scale;
  }

  static Colour toColour(const FColor& fc) {
    return Colour::fromFloatRGBA(red(fc), green(fc), blue(fc), fc.alpha());
  }

  static FColor fromColour(const Colour& c) {
    return FColor(c.getFloatRed(), c.getFloatGreen(), c.getFloatBlue(),
                  c.getFloatAlpha());
  }
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_RGB__
