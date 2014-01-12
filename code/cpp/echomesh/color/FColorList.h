#ifndef __ECHOMESH_COLOR_FCOLORLIST__
#define __ECHOMESH_COLOR_FCOLORLIST__

#include <algorithm>

#include "echomesh/color/FColor.h"

namespace echomesh {
namespace color {

class FColorList : public vector<FColor> {
 public:
  void copy(const FColorList& that) {
    *this = that;
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

#endif  // __ECHOMESH_COLOR_FCOLORLIST__
