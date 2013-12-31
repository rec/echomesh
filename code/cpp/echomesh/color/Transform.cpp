#include <math.h>

#include <map>

#include "echomesh/color/Transform.h"

using namespace std;

namespace echomesh {
namespace color {

namespace {

typedef map<string, FloatTransform> TransformMap;

float PI = 3.14159265358979f;
float E = 2.718281828;

float identity(float x) { return x; }
float reverse(float x) { return 1.0 - x; }
float square(float x) { return x * x; }

float sine(float x) {
  return (1 + sinf(PI * (x - 0.5f))) / 2.0f;
}

float arcsine(float x) {
  return 0.5 + asinf(2.0 * x - 1.0) / PI;
}

float exp(float x) {
  return (expf(x) - 1.0) / (E - 1.0);
}

float log(float x) {
  return logf((E - 1.0) * x + 1.0);
}

TransformMap makeTransforms() {
  TransformMap tm;

  tm["identity"] = FloatTransform(identity, identity);
  tm["reverse"] = FloatTransform(reverse, reverse);
  tm["square"] = FloatTransform(square, sqrtf);
  tm["sqrt"] = FloatTransform(sqrtf, square);
  tm["sin"] = FloatTransform(sine, arcsine);
  tm["exp"] = FloatTransform(exp, log);
  tm["log"] = FloatTransform(log, exp);

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
