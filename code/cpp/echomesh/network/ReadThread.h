#ifndef __ECHOMESH_READ_THREAD__
#define __ECHOMESH_READ_THREAD__

#include <stdio.h>

#include <map>
#include <vector>

#include "yaml-cpp/yaml.h"

namespace echomesh {

class LineGetter;

class ReadThread;

class ReadThread : public Thread {
 public:
  ReadThread();
  virtual ~ReadThread();
  virtual void run();

 protected:
  void parse(const string&);

  void addHandler(const string& name, Callback* cb) {
    messageMap_[name] = cb;
  }

  typedef std::map<string, Callback*> MessageMap;

  Node node_;
  string type_;
  StringArray accum_;
  MessageMap messageMap_;

  ScopedPointer<LineGetter> lineGetter_;

 private:
  CriticalSection lock_;
  DISALLOW_COPY_AND_ASSIGN(ReadThread);
};

}  // namespace echomesh

#endif // __ECHOMESH_READ_THREAD__
