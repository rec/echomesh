#pragma once

#include <functional>

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

class CTransform {
 public:
  virtual ~CTransform() {}
  virtual float apply(float x) const = 0;
  virtual float inverse(float x) const = 0;
};

CTransform* makeTransform(const string&);

vector<string> getTransformNames();

}  // namespace color
}  // namespace echomesh

