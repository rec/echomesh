#ifndef __ECHOMESH_COLOR_SPI__
#define __ECHOMESH_COLOR_SPI__

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

class FColorList;

enum Order {BGR_ORDER, BRG_ORDER, GBR_ORDER, GRB_ORDER, RBG_ORDER, RGB_ORDER,
            NONE = -1};
Order getOrder(const String& s);

void fillSpi(const FColorList&, uint8*, Order);

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_COLOR_SPI__
