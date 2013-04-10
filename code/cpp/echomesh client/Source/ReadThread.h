#ifndef __ECHOMESH_READ_THREAD__
#define __ECHOMESH_READ_THREAD__

#include <iostream>
#include <string>
#include <stdio.h>

#include "../JuceLibraryCode/JuceHeader.h"
#include "disallow.h"
#include "LightComponent.h"

namespace echomesh {

class ReadThread : public Thread {
 public:
  ReadThread(LightComponent* light) : Thread("ReadThread"), light_(light) {}

  virtual void run() {
    using namespace std;
    string s;
    String st;
    while (!feof(stdin)) {
      s.clear();
      getline(cin, s);
      if (s.empty())
        continue;
      st = s.c_str();

      int index = st.indexOfChar(':');
      cout << st;
      if (index > 0) {
        String cmd = st.substring(0, index);
        if (cmd == "q") {
          signalThreadShouldExit();
          JUCEApplication::quit();
          return;
        }
        String body = st.substring(index + 1).trim();
        StringArray parts;
        parts.addTokens(body, " ", "");
        if (cmd == "c")
          light_->setLights(parts);
        else if (cmd == "l")
          light_->setLayout(parts);
      }
    }
  }

 private:
  LightComponent* const light_;

  DISALLOW_COPY_AND_ASSIGN(ReadThread);
};


}  // namespace echomesh

#endif __ECHOMESH_READ_THREAD__
