#include "echomesh/color/HSB.h"
#include "echomesh/color/RGB.h"

namespace echomesh {
namespace color {

FColor HSB::fromRGB(const FColor& rgb) const {
  const auto brightness = jmax(RGB::red(rgb), RGB::green(rgb), RGB::blue(rgb));
  auto hue = 0.0f, saturation = 0.0f;

  if (not near(brightness, 0.0)) {
    const auto darkest = jmin(RGB::red(rgb), RGB::green(rgb), RGB::blue(rgb));
    const auto range = brightness - darkest;
    saturation = range / brightness;

    if (not near(saturation, 0.0)) {
      const float r = (brightness - RGB::red(rgb)) / range;
      const float g = (brightness - RGB::green(rgb)) / range;
      const float b = (brightness - RGB::blue(rgb)) / range;

      if (near(RGB::red(rgb), brightness))
        hue = b - g;
      else if (near(RGB::green(rgb), brightness))
        hue = 2.0f + r - b;
      else
        hue = 4.0f + g - r;

      hue /= 6.0f;

      if (hue < 0)
        hue += 1.0f;
    }
  }
  return FColor(hue, saturation, brightness, rgb.alpha());
}

// from http://www.cs.rit.edu/~ncs/color/t_convert.html
FColor HSB::toRGB(const FColor& hsb) const {
  auto h = hue(hsb), s = saturation(hsb), b = brightness(hsb);
  float r, g, bl;
 	if (s == 0) {
		// achromatic (grey)
		r = g = b = b;
	} else {
    h *= 6;			// sector 0 to 5
    int i = floor(h);
    auto f = h - i;			// factorial part of h
    auto p = b * (1 - s);
    auto q = b * (1 - s * f);
    auto t = b * (1 - s * (1 - f));

    switch(i) {
      case 0:
        r = b;
        g = t;
        bl = p;
        break;

      case 1:
        r = q;
        g = b;
        bl = p;
        break;

      case 2:
        r = p;
        g = b;
        bl = t;
        break;

      case 3:
        r = p;
        g = q;
        bl = b;
        break;

      case 4:
        r = t;
        g = p;
        bl = b;
        break;

      case 5:
      default:
        r = b;
        g = p;
        bl = q;
        break;
    }
  }

  return FColor(r, g, bl, hsb.alpha());
}

}  // namespace color
}  // namespace echomesh
