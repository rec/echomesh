#ifndef __ECHOMESH_READ_THREAD__
#define __ECHOMESH_READ_THREAD__

#include <stdio.h>

#include <vector>

#include "../JuceLibraryCode/JuceHeader.h"
#include "disallow.h"
#include "yaml-cpp/yaml.h"
#include "LightConfig.h"

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

  void quit();
  void clear();
  void parseLight(const YAML::Node&);
  void parseConfig(const YAML::Node&);
  void displayLights();
  void enforceSizes();

  LightComponent* const lightComponent_;
  YAML::Node node_;
  StringArray accum_;
  FILE* file_;
  ColorList colors_;
  ColorByteBank bytes_;
  ByteList colorBytes_;
  LightConfig config_;
  ColorBytes rgb_order_;
  double brightness_;

  DISALLOW_COPY_AND_ASSIGN(ReadThread);
};


}  // namespace echomesh

#endif __ECHOMESH_READ_THREAD__
