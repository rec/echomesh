#pragma once

#include <algorithm>

#include "echomesh/color/FColor.h"

namespace echomesh {
namespace color {

class FColorList : public vector<FColor> {
  public:
    FColor& at(size_t i) {
        DCHECK(isIndex(i)) << "Bad index " << i;
        return vector<FColor>::at(i);
    }

    void copy(const FColorList& that) {
        *this = that;
    }

    // DEPRECATED - use Combine.h.
    void combine(const FColorList& that) {
        resize(std::max(size(), that.size()));
        for (auto i = 0; i < that.size(); ++i)
            at(i).combine(that.get(i));
    }

    size_t count(const FColor& c) const {
        return std::count(begin(), end(), c);
    }

    void extend(const FColorList& that) {
        insert(end(), that.begin(), that.end());
    }

    void eraseOne(size_t pos) {
        erase(begin() + pos);
    }

    void eraseRange(size_t b, size_t e) {
        erase(begin() + b, begin() + e);
    }

    const FColor& get(size_t i) const {
        return isIndex(i) ? vector<FColor>::at(i) : FColor::BLACK;
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
            result.push_back(longer[i].interpolate(color, ratio, smooth, i));
        }

        return result;
    }

    long index(const FColor& c) const {
        auto i = std::find(begin(), end(), c);
        return i == end() ? -1 : i - begin();
    }

    void insertRange(size_t b1, const FColorList& from, size_t b2, size_t e2) {
        insert(begin() + b1, from.begin() + b2, from.begin() + e2);
    }

    bool isIndex(size_t i) const {
        return i < size();
    }

    void resize(unsigned long s) {
        vector<FColor>::resize(s, FColor::BLACK);
    }

    void reverse() {
        std::reverse(begin(), end());
    }

    void scale(float s) {
        for (auto& i: *this)
            i.scale(s);
    }

    void set(size_t pos, const FColor& color) {
        if (pos >= size())
            resize(pos + 1);
        LOG_IF(DFATAL, pos < 0) << "position is negative: " << pos;
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

class FColorArray : public FColorList {
  public:
    int columns() const { return columns_; }
    void setColumns(int columns) { columns_ = columns; }

    FColor& at(size_t x, size_t y) {
        return FColorList::at(index(x, y));
    }

    const FColor& get(size_t x, size_t y) const {
        return FColorList::get(index(x, y));
    }

    size_t index(size_t x, size_t y) const {
        return x + y * columns_;
    }

    bool isIndex(size_t x, size_t y) const {
        return FColorList::isIndex(index(x, y));
    }

    void set(size_t x, size_t y, const FColor& color) {
        FColorList::set(index(x, y), color);
    }

  private:
    int columns_ = 0;
};

}  // namespace color
}  // namespace echomesh
