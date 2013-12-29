#include "echomesh/color/ColorModel.h"
#include "echomesh/color/FColor.h"
#include "echomesh/color/HSB.h"
#include "echomesh/color/RGB.h"

namespace echomesh {
namespace color {

unique_ptr<ColorModel> ColorModel::RGB_MODEL(new RGB);
// HSB_MODEL;

}  // namespace color
}  // namespace echomesh
