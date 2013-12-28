#ifndef __ECHOMESH_FCOLOR__
#define __ECHOMESH_FCOLOR__

#include "echomesh/base/Echomesh.h"

namespace echomesh {

struct FColor {
  FColor() {}
  FColor(float red, float green, float blue, float alpha=1.0) : alpha_(alpha) {
    parts_[0] = red;
    parts_[1] = green;
    parts_[2] = blue;
  }

  const float* parts() const { return parts_; }
  float* parts() { return parts_; }

  const float& alpha() const { return alpha_; }
  float& alpha() { return alpha_; }

  const float& hue() const { return parts_[0]; }
  const float& saturation() const { return parts_[1]; }
  const float& brightness() const { return parts_[2]; }

  float& hue() { return parts_[0]; }
  float& saturation() { return parts_[1]; }
  float& brightness() { return parts_[2]; }

  bool operator==(const FColor& other) const;

  static FColor NO_COLOR;

  FColor toHSB() const;
  FColor fromHSB() const;
  FColor toYIQ() const;
  FColor fromYIQ() const;

 private:
  float parts_[3];
  float alpha_;

  friend struct RGB;
  friend struct HSB;
};

}  // namespace echomesh

#endif  // __ECHOMESH_FCOLOR__
