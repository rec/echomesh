#include "echomesh/color/ColorModel.h"
#include "echomesh/color/FColor.h"
#include "echomesh/color/HSB.h"
#include "echomesh/color/RGB.h"

namespace echomesh {
namespace color {

ColorModel* const ColorModel::RGB_MODEL = new RGB;
ColorModel* const ColorModel::HSB_MODEL = new HSB;

}  // namespace color
}  // namespace echomesh
