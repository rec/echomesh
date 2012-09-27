#include <string.h>
#include <iostream>

#include "ProcessLine.h"
#include "Commands.h"

using namespace std;

namespace echomesh {

namespace {

const char PLAY[] = "play ";
const char LIST[] = "list";

}  // namespace

void processCommandLine(const std::string& s) {
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

}  // namespace echomesh

