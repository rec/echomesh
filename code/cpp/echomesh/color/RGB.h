#ifndef __ECHOMESH_RGB__
#define __ECHOMESH_RGB__

#include "echomesh/color/FColor.h"
#include "echomesh/color/ColorModel.h"
#include "echomesh/color/ColorName.h"

namespace echomesh {
namespace color {

class RGB : public ColorModel {
 public:
  void combine(const FColor& x, FColor* y) const override { combineRGB(x, y); }

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
    return begin.interpolate(end, ratio);
  }

  static const float& red(const FColor& fc) { return fc.red(); }
  static const float& green(const FColor& fc) { return fc.green(); }
  static const float& blue(const FColor& fc) { return fc.blue(); }

  static float& red(FColor& fc) { return fc.red(); }
  static float& green(FColor& fc) { return fc.green(); }
  static float& blue(FColor& fc) { return fc.blue(); }

  static void combineRGB(const FColor& x, FColor* y) {
    red(*y) = std::max(red(*y), red(x));
    green(*y) = std::max(green(*y), green(x));
    blue(*y) = std::max(blue(*y), blue(x));
    y->alpha() = std::max(y->alpha(), x.alpha());
  }
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_RGB__
