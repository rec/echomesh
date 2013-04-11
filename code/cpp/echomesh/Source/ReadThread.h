#ifndef __ECHOMESH_READ_THREAD__
#define __ECHOMESH_READ_THREAD__

#include <stdio.h>

#include <vector>

#include "../JuceLibraryCode/JuceHeader.h"
#include "disallow.h"
#include "yaml-cpp/yaml.h"

namespace echomesh {

class LightComponent;

class ReadThread : public Thread {
 public:
  ReadThread(LightComponent* light);
  virtual ~ReadThread();

  virtual void run();

 private:
  void handleMessage();
  void parseNode();
  void parseColor(const YAML::Node&);
  void parseSettings(const YAML::Node&);

  LightComponent* const light_;
  StringArray accum_;
  YAML::Node node_;
  std::vector<uint8> lights_;
  FILE* file_;
  std::vector<Colour> colors_;

  DISALLOW_COPY_AND_ASSIGN(ReadThread);
};


}  // namespace echomesh

#endif __ECHOMESH_READ_THREAD__
