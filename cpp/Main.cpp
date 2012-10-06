#include <iostream>
#include <string>

#include "ProcessLine.h"

using namespace std;

int main(int argc, char **argv) {
  google::InitGoogleLogging(argv[0]);
  LOG(INFO) << "Synth starting";

  string s;
  while (getline(cin, s))
    echomesh::processCommandLine(s);
}
