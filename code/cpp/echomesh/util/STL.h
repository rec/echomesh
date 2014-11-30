#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {

template <typename Value, typename Container>
void erasePointer(Container* container, Value* v) {
    auto isCallback = [&](unique_ptr<Value> const& p) { return p.get() == v; };
    auto remover = remove_if(container->begin(), container->end(), isCallback);
    container->erase(remover, container->end());
}

}  // namespace echomesh
