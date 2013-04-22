#ifndef __ECHOMESH_LIGHT_READER__
#define __ECHOMESH_LIGHT_READER__

#include <stdio.h>

#include <istream>
#include <vector>

#include "echomesh/LightConfig.h"
#include "echomesh/ReadThread.h"

namespace echomesh {

class LightComponent;

class LightReader : public ReadThread {
 public:
  LightReader(LightComponent* light, const String& commandLine);
  virtual ~LightReader();

 private:
  void parseNode();

  virtual void quit();
  void clear();
  void parseLight(const YAML::Node&);
  void parseConfig(const YAML::Node&);
  void displayLights();
  void enforceSizes();

  uint8 getLedColor(float color) const;

  LightComponent* const lightComponent_;
  FILE* file_;
  ColorList colors_;
  ColorByteBank bytes_;
  ByteList colorBytes_;
  LightConfig config_;
  ColorBytes rgb_order_;
  float brightness_;

  DISALLOW_COPY_AND_ASSIGN(LightReader);
};


}  // namespace echomesh

#endif  // __ECHOMESH_LIGHT_READER__
