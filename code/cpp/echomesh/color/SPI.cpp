#include "echomesh/color/SPI.h"

#include "echomesh/color/FColorList.h"

namespace echomesh {
namespace color {

namespace {

const char* NAMES[] = {"BGR", "BRG", "GBR", "GRB", "RBG", "RGB"};

template <typename T>
void reorder(Order order, T& r, T& g, T& b) {
  T t;
  switch (order) {
    case BGR_ORDER:  t = r; r = b; b = g; g = t; break;
    case BRG_ORDER:  t = r; r = b; g = b; b = t; break;
    case GBR_ORDER:  t = r; r = g; g = b; b = t; break;
    case GRB_ORDER:  t = r; r = g; g = t; break;
    case RBG_ORDER:  t = g; g = b; b = t; break;
    case RGB_ORDER:  break;
    default:
      LOG(ERROR) << "Don't understand order " << order;
  }
}

uint8 toLight(float x) {
  return std::min(static_cast<int>((0x7F + 0.1f) * x), 0x7f);
}

}  // namespace

Order getOrder(const String& s) {
  auto t = s.toUpperCase();
  for (auto& name: NAMES) {
    if (t == name)
      return static_cast<Order>(&name - NAMES);
  }
  return NONE;
}

void fillSpi(const FColorList& fc, uint8* bytes, Order o) {
  auto i = 0;
  for (auto color: fc) {
    auto red = toLight(color.red());
    auto green = toLight(color.green());
    auto blue = toLight(color.blue());

    reorder(o, red, green, blue);
    bytes[i++] = red;
    bytes[i++] = green;
    bytes[i++] = blue;
  }
}

}  // namespace color
}  // namespace echomesh
