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
    resize(std::max(size(), that.size()), FColor::BLACK);
    for (auto i = 0; i < size(); ++i)
      at(i).combine(that.get(i));
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

  const FColor& get(int i) const {
    return (i >= 0 and i < size()) ? at(i) : FColor::BLACK;
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

  void set(int pos, const FColor& color) {
    if (pos >= size())
      resize(pos + 1, FColor::BLACK);
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

