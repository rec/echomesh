#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace audio {

template <typename Number>
class RingBufferIndex {
 public:
  explicit RingBufferIndex(Number size)
      : size_(size), begin_(0), end_(0), justWrote_(false) {
  }

  typedef std::pair<Number, Number> Block;
  typedef std::vector<Block> Blocks;

  Blocks write(Number count) {
    Blocks result;
    count = std::min(count, size_);
    auto overruns = available() - count;

    if (overruns > 0)
      begin_ = limit(begin_ + overruns);

    while (count > 0) {
      auto e = wraps() ? begin_ : size_;
      auto c = std::min(count, e - end_);
      CHECK_GT(c, 0) << e << ", " << c;
      append(&result, end_, end_ + c);
      end_ = limit(end_ + c);
      count -= c;
    }

    justWrote_ = true;
    return result;
  }

  Blocks read(Number count) {
    Blocks result;
    count = std::min(count, available());
    auto b = begin_;
    auto e = end_ + pad();

    while (count > 0) {
      auto split = (b < end_) and (e > end_);
      auto c = std::min(count, (split ? end_ : e) - b);
      append(&result, b, b + c);
      b += c;
      count -= c;
    }
    begin_ = limit(b);

    justWrote_ = false;
    return result;
  }

  Number size() const { return size_; }
  Number available() const { return pad() + end_ - begin_; }
  Number begin() const { return begin_; }
  Number end() const { return end_; }

 private:
  bool wraps() const {
    return begin_ > end_ or (begin_ == end_ and justWrote_);
  }

  Number pad() const {
    return wraps() ? size_ : 0;
  }

  Number limit(Number x) const {
    return (x < size_) ? x : (x - size_);
  }

  void append(Blocks* blocks, Number b, Number e) {
    blocks->emplace_back(limit(b), (e == size_) ? e : limit(e));
  }

  const Number size_;
  Number begin_, end_;
  bool justWrote_;

  DISALLOW_COPY_ASSIGN_AND_LEAKS(RingBufferIndex);
};

}  // namespace audio
}  // namespace echomesh
