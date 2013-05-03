#ifndef __ECHOMESH_LIGHT_READER__
#define __ECHOMESH_LIGHT_READER__

#include <stdio.h>

#include <istream>
#include <vector>

#include "echomesh/base/LightConfig.h"
#include "echomesh/network/ReadThread.h"

namespace echomesh {

class LightingWindow;

class LightReader : public ReadThread {
 public:
  LightReader(LightingWindow* window, const String& commandLine);
  virtual ~LightReader();

 private:
  virtual void quit();
  void clear();
  void light();
  void config();
  void setVisible(bool isVisible);
  void displayLights();
  void enforceSizes();

  uint8 getLedColor(float color) const;

  LightingWindow* const lightingWindow_;
  FILE* file_;
  bool compressed_;
  ColorList colors_;
  ColorByteBank bytes_;
  ByteList colorBytes_;
  LightConfig config_;
  ColorBytes rgbOrder_;
  float brightness_;
  bool configReceived_;

  DISALLOW_COPY_AND_ASSIGN(LightReader);
};


}  // namespace echomesh

#endif  // __ECHOMESH_LIGHT_READER__
