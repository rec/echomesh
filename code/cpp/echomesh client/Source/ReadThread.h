#ifndef __ECHOMESH_READ_THREAD__
#define __ECHOMESH_READ_THREAD__

#include <iostream>
#include <iostream>
#include <string>

#include "../JuceLibraryCode/JuceHeader.h"
#include "disallow.h"

namespace echomesh {

class ReadThread : public Thread {
 public:
  ReadThread() : Thread("ReadThread") {}

  virtual void run() {
    using namespace std;
    string s;
    while (!feof(stdin)) {
      s.clear();
      getline(cin, s);
      printf("%s", s.c_str());
    }
  }

 private:
  DISALLOW_COPY_AND_ASSIGN(ReadThread);
};


}  // namespace echomesh

#endif __ECHOMESH_READ_THREAD__
