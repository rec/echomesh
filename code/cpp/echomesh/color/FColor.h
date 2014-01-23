#ifndef __ECHOMESH_FCOLOR__
#define __ECHOMESH_FCOLOR__

#include <math.h>

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

class FColor {
 public:
  FColor() {}

  FColor(float red, float green, float blue, float alpha=1.0)
      : red_(red), green_(green), blue_(blue), alpha_(alpha) {
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

  FColor(const Colour& c)
      : red_(c.getFloatRed()),
        green_(c.getFloatGreen()),
        blue_(c.getFloatBlue()),
        alpha_(c.getFloatAlpha()) {
  }

  const float& red() const { return red_; }
  const float& green() const { return green_; }
  const float& blue() const { return blue_; }

  float& red() { return red_; }
  float& green() { return green_; }
  float& blue() { return blue_; }

  const float& alpha() const { return alpha_; }
  float& alpha() { return alpha_; }

  void clear() {
    red_ = green_ = blue_ = 0.0f;
    alpha_ = 1.0f;
  }

  static const FColor make_black() {
    FColor black;
    black.clear();
    return black;
  }

  static const FColor& black() {
    static FColor BLACK = make_black();
    return BLACK;
  }

  void gamma(float f) {
    red_ = powf(red_, f);
    green_ = powf(green_, f);
    blue_ = powf(blue_, f);
  }

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

  Colour toColour() const {
    return Colour(floatToUInt8(red()),
                  floatToUInt8(green()),
                  floatToUInt8(blue()),
                  floatToUInt8(alpha()));
  }

  FColor interpolate(const FColor& end, float ratio) const {
    auto b0 = red_, b1 = green_, b2 = blue_;
    auto e0 = end.red_, e1 = end.green_, e2 = end.blue_;
    return FColor(b0 + ratio * (e0 - b0),
                  b1 + ratio * (e1 - b1),
                  b2 + ratio * (e2 - b2));
  }

  void scale(float scale) {
    red_ *= scale;
    green_ *= scale;
    blue_ *= scale;
  }

  struct Comparer {
    bool operator()(const FColor& x, const FColor& y) { return x.compare(y) < 0; }
  };

  static uint8 floatToUInt8(const float n) {
    return static_cast<uint8>(jmax(0.0f, jmin(255.0f, n * 255.1f)));
  }

  void combine(const FColor& x) {
    red_ = std::max(red_, x.red());
    green_ = std::max(green_, x.green());
    blue_ = std::max(blue_, x.blue());
    alpha_ = std::max(alpha_, x.alpha_);
  }

 private:
  float red_, green_, blue_, alpha_;
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_FCOLOR__
