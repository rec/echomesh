#include "MakeTimerSpec.h"

using namespace std;

namespace echomesh {

itimerspec makeTimerSpec(const string& s) {
  itimerspec spec = {};
  timespec* value = &spec.it_value;

  char* endptr;
  value->tv_sec = strtol(s.c_str(), &endptr, 10);
  if (*endptr == '.') {
    string t((string(endptr + 1) + "000000000").substr(0, 9));
    value->tv_nsec = strtol(t.c_str(), &endptr, 10);
    if (*endptr)
      cerr << "Didn't understand nanoseconds in time " << s << endl;
  } else if (*endptr) {
    cerr << "Didn't understand time " << s << endl;
  }

  return spec;
}

}  // namespace echomesh
