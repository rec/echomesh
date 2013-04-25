#ifndef __ECHOMESH_READ_THREAD__
#define __ECHOMESH_READ_THREAD__

#include <stdio.h>

#include <istream>
#include <map>
#include <vector>

#include "yaml-cpp/yaml.h"
#include "echomesh/base/LightConfig.h"

namespace echomesh {

class LineGetter;

class ReadThread;

class ReadThread : public Thread {
 public:
  ReadThread(const String& commandLine);
  virtual ~ReadThread();
  virtual void run();
  void handleMessage(const string&);
  virtual void quit() = 0;
  void registerCallback(const string& name, Callback* cb) {
    messageMap_[name] = cb;
  }

 protected:
  virtual void parseNode() {}

  typedef std::map<string, Callback*> MessageMap;

  YAML::Node node_;
  string type_;
  StringArray accum_;
  MessageMap messageMap_;

  ScopedPointer<LineGetter> lineGetter_;

  DISALLOW_COPY_AND_ASSIGN(ReadThread);
};

}  // namespace echomesh

#endif // __ECHOMESH_READ_THREAD__
