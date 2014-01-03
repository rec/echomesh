#ifndef __ECHOMESH_FCOLOR__
#define __ECHOMESH_FCOLOR__

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

class FColor {
 public:
  FColor() {}

  FColor(float x, float y, float z, float alpha=1.0) : alpha_(alpha) {
    parts_[0] = x;
    parts_[1] = y;
    parts_[2] = z;
  }

  FColor(uint32 parts) {
    parts_[2] = parts & 0xFF;
    parts >>= 8;
    parts_[1] = parts & 0xFF;
    parts >>= 8;
    parts_[0] = parts & 0xFF;
    parts >>= 8;
    alpha_ = parts;
  }

  const float* parts() const { return parts_; }
  float* parts() { return parts_; }

  const float& alpha() const { return alpha_; }
  float& alpha() { return alpha_; }

  void copy(const FColor& other) { *this = other; }
  void copy(const FColor* other) { copy(*other); }
  bool operator==(const FColor& other) const { return not compare(other); }

  int compare(const FColor& x) const {
    if (this != &x) {
      for (auto i = 0; i < 3; ++i) {
        if (not near(parts_[i], x.parts_[i])) {
          if (parts_[i] < x.parts_[i])
            return -1;
          if (parts_[i] > x.parts_[i])
            return 1;
        }
      }
      if (alpha() < x.alpha())
        return -1;
      if (alpha() > x.alpha())
        return 1;
    }
    return 0;
  }

#if 0
  FColor interpolate(const FColor& end, float ratio) const {
    auto b0 = parts_[0], b1 = parts_[1], b2 = parts_[2];
    auto e0 = end.parts_[0], e1 = end.parts_[1], e2 = end.parts_[2];
    return FColor(b0 + ratio * (e0 - b0),
                  b1 + ratio * (e1 - b1),
                  b2 + ratio * (e2 - b2));
  }
#endif

  struct Comparer {
    bool operator()(const FColor& x, const FColor& y) { return x.compare(y) < 0; }
  };

 private:
  float parts_[3];
  float alpha_;
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_FCOLOR__
