#ifndef __ECHOMESH_HSB__
#define __ECHOMESH_HSB__

#include "echomesh/color/ColorModel.h"
#include "echomesh/color/FColor.h"

namespace echomesh {
namespace color {

class HSB : public ColorModel {
  void scale(FColor*, float) const override {
  }

  void combine(const FColor&, FColor*) const override {
  }

  string toName(const FColor&) const override {
    return "";
  }

  bool fromName(const string&, FColor*) const override {
    return false;
  }

  static const float& hue(const FColor& c) { return c.parts()[0]; }
  static const float& saturation(const FColor& c) { return c.parts()[1]; }
  static const float& brightness(const FColor& c) { return c.parts()[2]; }

  static float& hue(FColor& c) { return c.parts()[0]; }
  static float& saturation(FColor& c) { return c.parts()[1]; }
  static float& brightness(FColor& c) { return c.parts()[2]; }

  static FColor fromRGB(const FColor&);
  static FColor toRGB(const FColor&);
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_HSB__
