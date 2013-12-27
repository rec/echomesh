#ifndef __ECHOMESH_FCOLOR__
#define __ECHOMESH_FCOLOR__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

struct FColor {
  FColor() {}
  FColor(float red, float green, float blue, float alpha=1.0)
      : x_(red), y_(green), z_(blue), alpha_(alpha) {
  }

  const float& alpha() const { return alpha_; }
  float& alpha() { return alpha_; }

  const float& red() const { return x_; }
  const float& green() const { return y_; }
  const float& blue() const { return z_; }

  float& red() { return x_; }
  float& green() { return y_; }
  float& blue() { return z_; }

  const float& hue() const { return x_; }
  const float& saturation() const { return y_; }
  const float& brightness() const { return z_; }

  float& hue() { return x_; }
  float& saturation() { return y_; }
  float& brightness() { return z_; }

  bool operator==(const FColor& other) const;

  static FColor NO_COLOR;

  FColor toHSB() const;
  FColor fromHSB() const;
  FColor toYIQ() const;
  FColor fromYIQ() const;

 private:
  float x_, y_, z_, alpha_;

  friend struct RGB;
  friend struct HSB;
};

}  // namespace echomesh

#endif  // __ECHOMESH_FCOLOR__
