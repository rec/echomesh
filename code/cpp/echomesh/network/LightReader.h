#ifndef __ECHOMESH_LIGHT_READER__
#define __ECHOMESH_LIGHT_READER__

#include <stdio.h>

#include <istream>
#include <vector>

#include "echomesh/base/LightConfig.h"
#include "echomesh/network/ReadThread.h"

namespace echomesh {

class LightComponent;

class LightReader : public ReadThread {
 public:
  LightReader(LightComponent* light, const String& commandLine);
  virtual ~LightReader();

 private:
  virtual void quit();
  void clear();
  void clight();
  void light();
  void config();
  void displayLights();
  void enforceSizes();

  uint8 getLedColor(float color) const;

  LightComponent* const lightComponent_;
  bool compressed_;
  FILE* file_;
  ColorList colors_;
  ColorByteBank bytes_;
  ByteList colorBytes_;
  LightConfig config_;
  ColorBytes rgbOrder_;
  float brightness_;

  DISALLOW_COPY_AND_ASSIGN(LightReader);
};


}  // namespace echomesh

#endif  // __ECHOMESH_LIGHT_READER__
