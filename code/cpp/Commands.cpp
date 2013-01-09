#include <iostream>
#include <vector>

#include "Commands.h"

#include "MakeTimerSpec.h"
#include "Split.h"

using namespace std;

namespace echomesh {

void play(const string& s) {
  vector<string> parts;
  split(s, &parts);
  if (parts.size() == 2) {
    makeTimerSpec(parts[1]);
  } else {
    cerr << "Needed to find 2 fields in '" << s
         << "' but found " << parts.size() << endl;
  }
}

void list() {
  cout << "Listing" << endl;
}

void error(const string& s) {
  cerr << "error: " << s << endl;
}

}  // namespace echomesh

