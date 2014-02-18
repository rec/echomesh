#pragma once

#include <functional>

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

typedef std::function<float(float)> FloatFunction;
typedef std::pair<FloatFunction, FloatFunction> FloatTransform;

class CTransform {
 public:
  CTransform(const FloatTransform& ft) : floatTransform_(ft) {}

  float apply(float x) const { return floatTransform_.first(x); }
  float inverse(float x) const { return floatTransform_.second(x); }

 private:
  FloatTransform const floatTransform_;
};

CTransform* makeTransform(const string&);

vector<string> getTransformNames();

}  // namespace color
}  // namespace echomesh

