#include <string.h>

#include <iostream>

using namespace std;

namespace {

const char PLAY[] = "play ";
const char LIST[] = "list";

void play(const string& s) {
  cout << "Playing: " << s << endl;
}

void list() {
  cout << "Listing" << endl;
}

void error(const string& s) {
  cerr << "error: " << s << endl;
}

}

int main(int argc, char **argv) {
  cout << "Synth starting" << endl;

  string s;
  while (getline(cin, s)) {
    bool err = false;
    if (!s.find(PLAY))
      play(s.substr(strlen(PLAY)));
    else if (!s.find(LIST))
      list();
    else
      err = true;

    if (err)
      error(s);
    else
      cout << "ok" << endl;
  }
}
