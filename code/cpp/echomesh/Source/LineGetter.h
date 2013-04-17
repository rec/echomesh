#ifndef __ECHOMESH_LINE_GETTER__
#define __ECHOMESH_LINE_GETTER__

#include <stdio.h>

#include <istream>
#include <iostream>
#include <fstream>
#include <string>
#include <queue>

#include "Echomesh.h"
#include "yaml-cpp/yaml.h"
#include "LightConfig.h"

namespace echomesh {

class LineGetter {
 public:
  LineGetter() {}
  virtual ~LineGetter() {}
  virtual string getLine() = 0;
  virtual bool eof() const = 0;
};

LineGetter* makeLineGetter(const String& commandLine);

}  // namespace echomesh

#endif __ECHOMESH_LINE_GETTER__
