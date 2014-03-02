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
  auto value = 0x7F + static_cast<int>(0x80 * x);
  return std::max(std::min(value, 0xFF), 0x7f);
}

}  // namespace

Order getOrder(const string& s) {
  string t = s;
  for (auto& ch: t)
    ch = toupper(ch);
  for (auto& name: NAMES) {
    if (t == name)
      return static_cast<Order>(&name - NAMES);
  }
  return NONE;
}

void fillSpi(const FColorList& fc, char* data, int length, Order o) {
  auto bytes = reinterpret_cast<uint8*>(data);
  auto i = 0;
  auto tail = length - 3;
  for (auto color: fc) {
    auto red = toLight(color.red());
    auto green = toLight(color.green());
    auto blue = toLight(color.blue());

    reorder(o, red, green, blue);
    bytes[i++] = red;
    bytes[i++] = green;
    bytes[i++] = blue;
    if (i >= tail)
      break;
  }

  for (; i < tail; ++i)
    bytes[i] = 0x7f;

  for (i = tail; i < length; ++i)
    bytes[i] = 0;
}

}  // namespace color
}  // namespace echomesh
