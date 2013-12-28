#include <algorithm>
#include <map>

#include "echomesh/color/Colors.h"

using namespace std;

namespace echomesh {

FColor interpolate(
    const FColor& begin, const FColor& end, float ratio) {
  auto br = RGB::red(begin), bg = RGB::green(begin), bb = RGB::blue(begin);
  auto er = RGB::red(end), eg = RGB::green(end), eb = RGB::blue(end);
  return FColor(br + ratio * (er - br),
                bg + ratio * (eg - bg),
                bb + ratio * (eb - bb));
}

void fillFColorList(
    FColorList* cl, const FColor& begin, const FColor& end, int size) {
  cl->resize(size);
  for (auto i = 0; i < size; ++i)
    cl->at(i) = interpolate(begin, end, i / (size - 1.0));
}

}  // namespace echomesh
