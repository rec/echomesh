#ifndef __ECHOMESH_COLOR_COLORMODEL__
#define __ECHOMESH_COLOR_COLORMODEL__

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

class FColor;

class ColorModel {
 public:
  ColorModel() {}
  virtual ~ColorModel() {}

  virtual void combine(const FColor&, FColor*) const = 0;
  virtual FColor interpolate(
      const FColor& begin, const FColor& end, float ratio) const = 0;
  virtual void scale(FColor*, float) const = 0;

  virtual string toName(const FColor&) const = 0;
  virtual bool fromName(const string&, FColor*) const = 0;
  virtual FColor toRGB(const FColor&) const = 0;
  virtual FColor fromRGB(const FColor&) const = 0;

  enum Model { RGB, HSV };
  static const ColorModel* getColorModel(Model);
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_COLOR_COLORMODEL__
