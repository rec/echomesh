#include <iostream>
#include <string>

#include "ProcessLine.h"

using namespace std;

int main(int argc, char **argv) {
  cout << "Synth starting" << endl;

  string s;
  while (getline(cin, s))
    echomesh::processCommandLine(s);
}
