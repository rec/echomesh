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

  virtual FColor interpolate(
      const FColor& begin, const FColor& end, float ratio) const = 0;

  virtual bool isRgb() const = 0;
  virtual FColor toRgb(const FColor&) const = 0;
  virtual FColor fromRgb(const FColor&) const = 0;
  virtual string modelName() const = 0;

  enum Model { RGB, HSB };
  static const ColorModel* getColorModel(Model);
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_COLOR_COLORMODEL__
