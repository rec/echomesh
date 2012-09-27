#include <stdlib.h>
#include <iostream>

#include "MakeTimerSpec.h"

using namespace std;

namespace echomesh {

itimerspec makeTimerSpec(const string& s) {
  itimerspec spec = {};
  timespec* value = &spec.it_value;

  char* endptr;
  value->tv_sec = strtol(s.c_str(), &endptr, 10);
  if (*endptr == '.') {
    string t((string(endptr) + "000000000").substr(0, 9));
    value->tv_nsec = strtol(t.c_str(), &endptr, 10);
    if (*endptr)
      cerr << "Didn't understand nanoseconds in time " << t;
  } else if (*endptr) {
    cerr << "Didn't understand time " << s;
  }

  return spec;
}

}  // namespace echomesh
