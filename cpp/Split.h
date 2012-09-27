#ifndef __ECHOMESH__SPLIT__
#define __ECHOMESH__SPLIT__

#include <string>

namespace echomesh {

template <class Container>
void split(const std::string& str, Container* parts,
              const std::string& delimiters = " ",
              const bool trimEmpty = false) {
  using namespace std;
  typedef typename Container::value_type Value;
  typedef typename Value::size_type Size;

  string::size_type pos, lastPos = 0;
  while (true) {
    pos = str.find_first_of(delimiters, lastPos);
    if (pos == string::npos) {
      pos = str.length();
      if (pos != lastPos || !trimEmpty)
        parts->push_back(Value(str.data() + lastPos, Size(pos -lastPos)));
      break;

    } else {
      if(pos != lastPos || !trimEmpty)
        parts->push_back(Value(str.data() + lastPos, Size(pos - lastPos)));
    }

    lastPos = pos + 1;
  }
}

}  // namespace echomesh

#endif  // __ECHOMESH__SPLIT__

