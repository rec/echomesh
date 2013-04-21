#ifndef __ECHOMESH_READ_THREAD__
#define __ECHOMESH_READ_THREAD__

#include <stdio.h>

#include <istream>
#include <vector>

#include "yaml-cpp/yaml.h"
#include "echomesh/LightConfig.h"

namespace echomesh {

class LineGetter;

class ReadThread : public Thread {
 public:
  ReadThread(const String& commandLine);
  virtual ~ReadThread();
  virtual void run();
  virtual void handleMessage(const string&) = 0;
  virtual void quit() = 0;

 protected:
  StringArray accum_;
  ScopedPointer<LineGetter> lineGetter_;

  DISALLOW_COPY_AND_ASSIGN(ReadThread);
};

}  // namespace echomesh

#endif // __ECHOMESH_READ_THREAD__
