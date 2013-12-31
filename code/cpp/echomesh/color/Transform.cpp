#include <map>

#include "echomesh/color/Transform.h"

namespace echomesh {
namespace color {

namespace {

typedef std::map<string, FloatTransform> TransformMap;

TransformMap makeTransforms() {
  TransformMap tm;
  return tm;
}

auto TRANSFORMS = makeTransforms();

}

const FloatTransform* getTransform(const string& name) {
  auto i = TRANSFORMS.find(name);
  return i == TRANSFORMS.end() ? nullptr : &i->second;
}

vector<string> getTransformNames() {
  vector<string> res;
  for (auto i: TRANSFORMS)
    res.push_back(i.first);
  return res;
}


}  // namespace color
}  // namespace echomesh
