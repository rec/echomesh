#ifndef __ECHOMESH_COLOR_TRANSFORM__
#define __ECHOMESH_COLOR_TRANSFORM__

#include <functional>

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

typedef std::function<float(float)> FloatFunction;
typedef std::pair<FloatFunction, FloatFunction> FloatTransform;

const FloatTransform* getTransform(const string&);
vector<string> getTransformNames();

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_COLOR_TRANSFORM__
