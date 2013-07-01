#ifndef __ECHOMESH_LINE_GETTER__
#define __ECHOMESH_LINE_GETTER__

#include <stdio.h>

#include <istream>
#include <iostream>
#include <fstream>
#include <string>
#include <queue>

#include "yaml-cpp/yaml.h"

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class LineGetter {
 public:
  LineGetter() {}
  virtual ~LineGetter() {}
  virtual string getLine() = 0;
  virtual bool eof() const = 0;
  virtual bool debug() const = 0;
};

LineGetter* makeLineGetter(const String& commandLine);

}  // namespace echomesh

#endif  // __ECHOMESH_LINE_GETTER__
