#include "echomesh/color/Mirror.h"

namespace echomesh {
namespace color {

FColorList mirror(
    const FColorList& fcl, unsigned int x, unsigned int y,
    bool reverseX, bool reverseY) {
    FColorList result;
    unsigned int size = fcl.size();
    result.resize(std::max(size, x * y));
    for (auto i = 0; i < result.size(); ++i) {
        auto my_y = i / x;
        auto my_x = i - (my_y * x);
        if (reverseX)
            my_x = x - my_x - 1;
        if (reverseY)
            my_y = y - my_y - 1;
        auto index = my_x * y + my_y;
        if (index < fcl.size())
            result[i] = fcl[index];
        else
            result[i].clear();
    }
    return result;
}

}  // namespace color
}  // namespace echomesh
