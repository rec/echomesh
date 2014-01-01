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

FloatTransform inverse(FloatTransform ft) {
  return FloatTransform(ft.second, ft.first);
}

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

FloatTransform power(float n) {
  return FloatTransform(
      bind(powf, placeholders::_1, n),
      bind(powf, placeholders::_1, 1 / n));
}

TransformMap makeTransforms() {
  TransformMap tm;

  tm["cube"] = power(3);
  tm["exp"] = FloatTransform(exp, log);
  tm["identity"] = FloatTransform(identity, identity);
  tm["log"] = FloatTransform(log, exp);
  tm["reverse"] = FloatTransform(reverse, reverse);
  tm["sine"] = FloatTransform(sine, arcsine);
  tm["sqrt"] = FloatTransform(sqrtf, square);
  tm["square"] = FloatTransform(square, sqrtf);

  return tm;
}

auto TRANSFORMS = makeTransforms();

FloatFunction compose(FloatFunction f, FloatFunction g) {
  return [&](float x) { return f(g(x)); };
}

FloatTransform compose(FloatTransform f, FloatTransform g) {
  return FloatTransform(compose(g.first, f.first), compose(f.second, g.second));
}

FloatTransform getOneTransform(const string& name) {
  auto i = TRANSFORMS.find(name);
  if (i != TRANSFORMS.end())
    return i->second;
  throw Exception("Can't understand transform " + name);
}

FloatTransform getTransform(const string& name) {
  StringArray parts;
  parts.addTokens(String(name), "+", "");
  if (not parts.size())
    throw Exception("Can't understand empty transform");

  FloatTransform result;
  for (auto i = 0; i < parts.size(); ++i) {
    auto p = parts[i].trim();
    if (p == "inverse") {
      if (not i)
        throw Exception("Transform: inverse can't be the first transform.");
      auto t = result.first;
      result.first = result.second;
      result.second = t;
    } else {
      auto tr = getOneTransform(p.toStdString());
      result = i ? compose(result, tr) : tr;
    }
  }

  return result;
}

}

CTransform* makeTransform(const string& s) {
  try {
    return new CTransform(getTransform(s));
  } catch (Exception e) {
    LOG(ERROR) << e.what();
    return nullptr;
  }
}

vector<string> getTransformNames() {
  vector<string> res;
  for (auto i: TRANSFORMS)
    res.push_back(i.first);
  return res;
}

}  // namespace color
}  // namespace echomesh
