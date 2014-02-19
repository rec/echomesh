#pragma once

#include <algorithm>

#include "echomesh/color/FColor.h"

namespace echomesh {
namespace color {

class FColorList : public vector<FColor> {
 public:
  void copy(const FColorList& that) {
    *this = that;
  }

  void combine(const FColorList& that) {
    int thisSize = size(), thatSize = that.size();
    if (thisSize >= thatSize) {
      for (auto i = 0; i < thatSize; ++i)
        (*this)[i].combine(that[i]);
    } else {
      resize(thatSize);
      for (auto i = 0; i < thisSize; ++i)
        (*this)[i].combine(that[i]);
      for (auto i = thisSize; i < thatSize; ++i)
        (*this)[i] = that[i];
    }
  }

  int count(const FColor& c) const {
    return std::count(begin(), end(), c);
  }

  void extend(const FColorList& that) {
    insert(end(), that.begin(), that.end());
  }

  void eraseOne(int pos) {
    erase(begin() + pos);
  }

  void eraseRange(int b, int e) {
    erase(begin() + b, begin() + e);
  }

  FColorList interpolate(
      const FColorList& that, float ratio,
      uint smooth = 0, uint index = 0) const {
    auto thatLonger = (size() < that.size());
    if (thatLonger)
      ratio = 1.0f - ratio;
    auto& longer = thatLonger ? that : *this;
    auto& shorter = thatLonger ? *this : that;
    FColorList result;
    result.reserve(longer.size());

    for (uint i = 0; i < longer.size(); ++i) {
      auto& color = (i < shorter.size()) ? shorter[i] : FColor::BLACK;
      result.push_back(longer[i].interpolate(color, ratio, i, smooth));
    }

    return result;
  }

  int index(const FColor& c) const {
    auto i = std::find(begin(), end(), c);
    return i == end() ? -1 : i - begin();
  }

  void insertRange(int b1, const FColorList& from, int b2, int e2) {
    insert(begin() + b1, from.begin() + b2, from.begin() + e2);
  }

  void reverse() {
    std::reverse(begin(), end());
  }

  void scale(float s) {
    for (auto& i: *this)
      i.scale(s);
  }

  void set(const FColor& color, int pos) {
    at(pos) = color;
  }

  void setAll(const FColor& fc) {
    for (auto& i: *this)
      i = fc;
  }

  void sort() {
    std::sort(begin(), end(), FColor::Comparer());
  }

  void gamma(float gamma) {
    for (auto color: *this)
      color.gamma(gamma);
  }
};

}  // namespace color
}  // namespace echomesh

