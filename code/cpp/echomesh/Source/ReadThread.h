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

class LightComponent;

class ReadThreadBase : public Thread {
 public:
  ReadThreadBase(const String& commandLine);
  virtual ~ReadThreadBase();
  virtual void run();
  virtual void handleMessage(const string&) = 0;
  virtual void quit() = 0;

 protected:
  std::istream* stream_;
  const String commandLine_;
  StringArray accum_;

  DISALLOW_COPY_AND_ASSIGN(ReadThreadBase);
};

class ReadThread : public ReadThreadBase {
 public:
  ReadThread(LightComponent* light, const String& commandLine);
  virtual ~ReadThread();

 private:
  virtual void handleMessage(const string&);
  void parseNode();

  virtual void quit();
  void clear();
  void parseLight(const YAML::Node&);
  void parseConfig(const YAML::Node&);
  void displayLights();
  void enforceSizes();

  uint8 getLedColor(float color) const;

  LightComponent* const lightComponent_;
  YAML::Node node_;
  FILE* file_;
  ColorList colors_;
  ColorByteBank bytes_;
  ByteList colorBytes_;
  LightConfig config_;
  ColorBytes rgb_order_;
  float brightness_;

  DISALLOW_COPY_AND_ASSIGN(ReadThread);
};


}  // namespace echomesh

#endif __ECHOMESH_READ_THREAD__
