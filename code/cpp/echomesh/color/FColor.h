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

  bool operator==(const FColor& other) const {
    return
        near(parts_[0], other.parts_[0]) and
        near(parts_[1], other.parts_[1]) and
        near(parts_[2], other.parts_[2]) and
        near(alpha_, other.alpha_);
  }
  static FColor NO_COLOR;

  FColor toHSB() const;
  FColor fromHSB() const;

 private:
  float parts_[3];
  float alpha_;

  friend struct RGB;
  friend struct HSB;
};

}  // namespace echomesh

#endif  // __ECHOMESH_FCOLOR__
