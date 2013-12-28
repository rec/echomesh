#ifndef __ECHOMESH_HSB__
#define __ECHOMESH_HSB__

#include "echomesh/color/FColor.h"

namespace echomesh {

struct HSB {
  static const float& hue(const FColor& c) { return c.parts_[0]; }
  static const float& saturation(const FColor& c) { return c.parts_[1]; }
  static const float& brightness(const FColor& c) { return c.parts_[2]; }

  static float& hue(FColor& c) { return c.parts_[0]; }
  static float& saturation(FColor& c) { return c.parts_[1]; }
  static float& brightness(FColor& c) { return c.parts_[2]; }

  static FColor fromRGB(const FColor&);
  static FColor toRGB(const FColor&);
};

}  // namespace echomesh

#endif  // __ECHOMESH_HSB__
