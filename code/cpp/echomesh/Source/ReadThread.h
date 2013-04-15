#ifndef __ECHOMESH_READ_THREAD__
#define __ECHOMESH_READ_THREAD__

#include <stdio.h>

#include <istream>
#include <vector>

#include "../JuceLibraryCode/JuceHeader.h"
#include "disallow.h"
#include "yaml-cpp/yaml.h"
#include "LightConfig.h"

namespace echomesh {

class ReadThread : public Thread {
 public:
  ReadThread(const String& commandLine);
  virtual ~ReadThread();
  virtual void run();
  virtual void handleMessage(const string&) = 0;
  virtual void quit() = 0;

 protected:
  std::istream* stream_;
  const String commandLine_;
  StringArray accum_;

  DISALLOW_COPY_AND_ASSIGN(ReadThread);
};

}  // namespace echomesh

#endif __ECHOMESH_READ_THREAD__
