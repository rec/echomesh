#ifndef __ECHOMESH_HSB__
#define __ECHOMESH_HSB__

#include "echomesh/color/ColorModel.h"
#include "echomesh/color/FColor.h"

namespace echomesh {
namespace color {

class HSB : public ColorModel {
  void scale(FColor* c, float f) const override {
    brightness(*c) *= f;
  }

  void combine(const FColor& f, FColor* t) const override {
    auto h1 = hue(f), h2 = hue(*t);
    hue(*t) = (h1 + h2) / 2;  // Guess?

    saturation(*t) = jmax(saturation(*t), saturation(f));
    brightness(*t) = jmax(brightness(*t), brightness(f));
  }

  string toName(const FColor& c) const override {
    return ColorModel::RGB_MODEL->toName(toRGB(c));
  }

  bool fromName(const string& s, FColor* c) const override {
    FColor rgb;
    bool success = ColorModel::RGB_MODEL->fromName(s, &rgb);
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
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_HSB__
