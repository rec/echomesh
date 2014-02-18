#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

class FColor;

bool nameToRgb(const String& cname, FColor*);
string rgbToName(const FColor&);

}  // namespace color
}  // namespace echomesh

