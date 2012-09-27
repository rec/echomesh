#include <string.h>


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
  }
}
