#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

class FColorList;

enum Order {BGR_ORDER, BRG_ORDER, GBR_ORDER, GRB_ORDER, RBG_ORDER, RGB_ORDER,
            NONE = -1};
Order getOrder(const string& s);

void fillSpi(const FColorList&, char*, size_t length, Order);

}  // namespace color
}  // namespace echomesh
