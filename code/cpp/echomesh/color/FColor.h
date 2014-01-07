#ifndef __ECHOMESH_FCOLOR__
#define __ECHOMESH_FCOLOR__

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

class FColor {
 public:
  FColor() {}

  FColor(float x, float y, float z, float alpha=1.0) : alpha_(alpha) {
    red_ = x;
    green_ = y;
    blue_ = z;
  }

  FColor(uint32 parts) {
    blue_ = parts & 0xFF;
    parts >>= 8;
    green_ = parts & 0xFF;
    parts >>= 8;
    red_ = parts & 0xFF;
    parts >>= 8;
    alpha_ = parts;
  }

  const float& red() const { return red_; }
  const float& green() const { return green_; }
  const float& blue() const { return blue_; }

  float& red() { return red_; }
  float& green() { return green_; }
  float& blue() { return blue_; }

  const float& alpha() const { return alpha_; }
  float& alpha() { return alpha_; }

  void copy(const FColor& other) { *this = other; }
  void copy(const FColor* other) { copy(*other); }
  bool operator==(const FColor& other) const { return not compare(other); }

  int compare(const FColor& x) const {
    if (this == &x)
      return 0;

    if (not near(red(), x.red())) {
      if (red() < x.red())
        return -1;
      if (red() > x.red())
        return 1;
    }
    if (not near(green(), x.green())) {
      if (green() < x.green())
        return -1;
      if (green() > x.green())
        return 1;
    }
    if (not near(blue(), x.blue())) {
      if (blue() < x.blue())
        return -1;
      if (blue() > x.blue())
        return 1;
    }
    if (alpha() < x.alpha())
        return -1;
      if (alpha() > x.alpha())
        return 1;
      return 0;
  }

#if 0
  FColor interpolate(const FColor& end, float ratio) const {
    auto b0 = red_, b1 = green_, b2 = blue_;
    auto e0 = end.red_, e1 = end.green_, e2 = end.blue_;
    return FColor(b0 + ratio * (e0 - b0),
                  b1 + ratio * (e1 - b1),
                  b2 + ratio * (e2 - b2));
  }
#endif

  struct Comparer {
    bool operator()(const FColor& x, const FColor& y) { return x.compare(y) < 0; }
  };

 private:
  float red_, green_, blue_, alpha_;
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_FCOLOR__
