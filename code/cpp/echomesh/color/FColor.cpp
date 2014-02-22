#include "echomesh/color/FColor.h"

namespace echomesh {
namespace color {

namespace {

const FColor make_black() {
  FColor black;
  black.clear();
  return black;
}

}

const FColor FColor::BLACK = make_black();

}  // namespace color
}  // namespace echomesh

