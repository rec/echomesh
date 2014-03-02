#include "echomesh/color/HSB.h"
#include "echomesh/color/RGB.h"

using namespace std;

namespace echomesh {
namespace color {

FColor HSB::hsbFromRgb(const FColor& rgb) {
  const auto brightness = max(
      max(RGB::red(rgb), RGB::green(rgb)), RGB::blue(rgb));
  auto hue = 0.0f, saturation = 0.0f;

  if (not near(brightness, 0.0)) {
    const auto darkest = min(
        min(RGB::red(rgb), RGB::green(rgb)), RGB::blue(rgb));
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
FColor HSB::hsbToRgb(const FColor& hsb) {
  auto h = hue(hsb), s = saturation(hsb), b = brightness(hsb);
  float red, green, blue;
 	if (s == 0) {
		// achromatic (grey)
		red = green = blue = b;
	} else {
    h *= 6;			// sector 0 to 5
    int i = floor(h);
    auto f = h - i;			// factorial part of h
    auto p = b * (1 - s);
    auto q = b * (1 - s * f);
    auto t = b * (1 - s * (1 - f));

    switch(i) {
      case 0:
        red = b;
        green = t;
        blue = p;
        break;

      case 1:
        red = q;
        green = b;
        blue = p;
        break;

      case 2:
        red = p;
        green = b;
        blue = t;
        break;

      case 3:
        red = p;
        green = q;
        blue = b;
        break;

      case 4:
        red = t;
        green = p;
        blue = b;
        break;

      case 5:
      default:
        red = b;
        green = p;
        blue = q;
        break;
    }
  }

  return FColor(red, green, blue, hsb.alpha());
}

}  // namespace color
}  // namespace echomesh
