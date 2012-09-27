#include <iostream>

#include "Commands.h"

using namespace std;

namespace echomesh {

void play(const string& s) {
  cout << "Playing: " << s << endl;
}

void list() {
  cout << "Listing" << endl;
}

void error(const string& s) {
  cerr << "error: " << s << endl;
}

}  // namespace echomesh

