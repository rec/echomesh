#pragma once

#include "echomesh/color/FColor.h"
#include "echomesh/color/RGB.h"

namespace echomesh {
namespace color {

class HSB : public ColorModel {
  public:
    string modelName() const override { return "hsb"; }

    FColor toRgb(const FColor& c) const override { return hsbToRgb(c); }
    FColor fromRgb(const FColor& c) const override { return hsbFromRgb(c); }

    bool isRgb() const override { return false; }

    FColor interpolate(
        const FColor& begin, const FColor& end, float ratio) const override {
        auto h0 = hue(begin), s0 = saturation(begin), b0 = brightness(begin),
                a0 = begin.alpha();
        auto h1 = hue(end), s1 = saturation(end), b1 = brightness(end),
                a1 = end.alpha();
        return FColor(
            interpolateHue(h0, h1, ratio),
            s0 + ratio * (s1 - s0),
            b0 + ratio * (b1 - b0),
            a0 + ratio * (a1 - a0));
    }

    static float interpolateHue(float x, float y, float r) {
        if (fabs(x - y) <= 0.5) {
            return x + (y - x) * r;
        }

        float res = (x < y) ? (1 + x) - r * (1 + x - y) : x + r * (1 + y - x);
        return res - floorf(res);
    }

    static const float& hue(const FColor& c) { return c.red(); }
    static const float& saturation(const FColor& c) { return c.green(); }
    static const float& brightness(const FColor& c) { return c.blue(); }

    static float& hue(FColor& c) { return c.red(); }
    static float& saturation(FColor& c) { return c.green(); }
    static float& brightness(FColor& c) { return c.blue(); }

    static void combineHSB(const FColor& f, FColor* t) {
        auto bf = brightness(f), bt = brightness(*t), btotal = bf + bt;
        if (near(btotal, 0.0f))
            hue(*t) = 0.0f;
        else
            hue(*t) = interpolateHue(hue(f), hue(*t), bf / btotal);
        saturation(*t) = std::max(saturation(*t), saturation(f));
        brightness(*t) = std::max(bf, bt);
        t->alpha() = std::max(t->alpha(), f.alpha());
    }

    static FColor hsbToRgb(const FColor&);
    static FColor hsbFromRgb(const FColor&);
};

}  // namespace color
}  // namespace echomesh

