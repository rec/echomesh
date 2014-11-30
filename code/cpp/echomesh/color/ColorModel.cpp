#include "echomesh/color/ColorModel.h"
#include "echomesh/color/FColor.h"
#include "echomesh/color/HSB.h"
#include "echomesh/color/RGB.h"

namespace echomesh {
namespace color {

static const ColorModel* const COLOR_MODELS[2] = { new RGB, new HSB };

const ColorModel* ColorModel::getColorModel(ColorModel::Model model) {
    return COLOR_MODELS[model];
}

}  // namespace color
}  // namespace echomesh
