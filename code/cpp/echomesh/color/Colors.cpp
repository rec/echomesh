#include <algorithm>
#include <map>

#include "echomesh/color/Colors.h"

using namespace std;

namespace echomesh {

struct FCompare {
  bool operator()(const FColor& x, const FColor& y) const {
    return RGB::compare(x, y) < 0;
  }
};

void sortFColorList(vector<FColor>* colorList) {
  std::sort(colorList->begin(), colorList->end(), FCompare());
}

int countColorsInList(const FColorList& cl, const FColor& c) {
  return std::count(cl.begin(), cl.end(), c);
}

int indexColorInList(const FColorList& cl, const FColor& c) {
  auto i = std::find(cl.begin(), cl.end(), c);
  return i == cl.end() ? -1 : i - cl.begin();
}

void reverseFColorList(FColorList* cl) {
  std::reverse(cl->begin(), cl->end());
}

int compareColors(const FColor& x, const FColor& y) {
  if (RGB::red(x) < RGB::red(y))
    return -1;
  if (RGB::red(x) > RGB::red(y))
    return 1;
  if (RGB::green(x) < RGB::green(y))
    return -1;
  if (RGB::green(x) > RGB::green(y))
    return 1;
  if (RGB::blue(x) < RGB::blue(y))
    return -1;
  if (RGB::blue(x) > RGB::blue(y))
    return 1;
  if (x.alpha() < y.alpha())
    return -1;
  if (x.alpha() > y.alpha())
    return 1;
  return 0;
}

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
