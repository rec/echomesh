#include <math.h>

#include <map>

#include "echomesh/color/Transform.h"

using namespace std;

namespace echomesh {
namespace color {

namespace {

typedef std::function<float(float)> FloatFunction;
typedef std::pair<FloatFunction, FloatFunction> FloatTransform;

class CTransformBase : public CTransform {
 public:
  explicit CTransformBase(const FloatTransform& ft) : floatTransform_(ft) {}

  float apply(float x) const override { return floatTransform_.first(x); }
  float inverse(float x) const override { return floatTransform_.second(x); }

 private:
  FloatTransform const floatTransform_;
  // DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(CTransformBase);
  // See https://github.com/rec/echomesh/issues/512
};

class Inverse : public CTransform {
 public:
  explicit Inverse(unique_ptr<CTransform> t) : transform_(move(t)) {}

  float apply(float x) const override { return transform_->inverse(x); }
  float inverse(float x) const override { return transform_->apply(x); }

 private:
  unique_ptr<CTransform> transform_;
  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(Inverse);
};

class Compose : public CTransform {
 public:
  Compose(unique_ptr<CTransform> first, unique_ptr<CTransform> second)
      : first_(move(first)), second_(move(second)) {
  }

  float apply(float x) const override {
    return second_->apply(first_->apply(x));
  }

  float inverse(float x) const override {
    return first_->inverse(second_->inverse(x));
  }

 private:
  unique_ptr<CTransform> first_, second_;
  DISALLOW_COPY_ASSIGN_EMPTY_AND_LEAKS(Compose);
};

unique_ptr<CTransform> compose(
    unique_ptr<CTransform> first, unique_ptr<CTransform> second) {
  if (not first.get())
    return move(second);
  if (not second.get())
    return move(first);
  return unique_ptr<CTransform>(new Compose(move(first), move(second)));
}

unique_ptr<CTransform> inverse(unique_ptr<CTransform> transform) {
  if (not transform.get())
    throw Exception("Invert cannot be the first transform.");
  return unique_ptr<CTransform>(new Inverse(move(transform)));
}

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

unique_ptr<CTransform> getOneTransform(const string& name) {
  auto i = TRANSFORMS.find(name);
  if (i == TRANSFORMS.end())
    throw Exception("Can't understand transform " + name);
  return unique_ptr<CTransform>(new CTransformBase(i->second));
}

unique_ptr<CTransform> getTransform(const string& name) {
  unique_ptr<CTransform> result;

  string token;
  for (auto i = 0; i <= name.size(); ++i) {
    auto ch = name.c_str()[i];
    if (ch and (not isspace(ch)) and (ch != '+')) {
      token.push_back(ch);
    } else if (not token.empty()) {
      if (token == "inverse")
        result = inverse(move(result));
      else
        result = compose(move(result), move(getOneTransform(token)));
      token.clear();
    }
  }
  return move(result);
}

}

CTransform* makeTransform(const string& s) {
  try {
    return getTransform(s).release();
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
