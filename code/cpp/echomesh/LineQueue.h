#ifndef __ECHOMESH_LINE_QUEUE__
#define __ECHOMESH_LINE_QUEUE__

#include <queue>

#include "echomesh/Echomesh.h"

namespace echomesh {

// Put in a sequence of strings containing some number of embedded "\n"
// characters, and get out a queue of lines terminated by "\n".
class LineQueue {
 public:
  LineQueue() {}

  bool empty() const { return lines_.empty(); }

  void push(const string& read) {
    if (read.empty())
      return;

    int begin = 0;
    while (int end = read.find('\n', begin) + 1) {
      lines_.push(read.substr(begin, end - begin));
      if (!carry_.empty()) {
        lines_.back() = carry_ + lines_.back();
        carry_.clear();
      }
      begin = end;
    }

    if (begin < read.size())
      carry_ = read.substr(begin);
  }

  string pop() {
    string result = lines_.front();
    lines_.pop();
    return result;
  }

 private:
  std::queue<string> lines_;
  string carry_;
};

}  // namespace echomesh

#endif  // __ECHOMESH_LINE_QUEUE__
