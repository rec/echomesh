#ifndef __ECHOMESH_LIGHT_CONTROLLER__
#define __ECHOMESH_LIGHT_CONTROLLER__

#include "echomesh/base/Config.h"

namespace echomesh {

class LightingWindow;

class LightController {
 public:
  LightController(LightingWindow*, const Node&);
  virtual ~LightController();

  void clear();
  void config();
  void displayLights();
  void enforceSizes();
  void light();

  uint8 getLedColor(float color) const;

  LightingWindow* const lightingWindow_;
  const Node& node_;

  FILE* file_;
  bool compressed_;
  ColorList colors_;
  ByteList colorBytes_;
  Config config_;
  ColorBytes rgbOrder_;
  float brightness_;

  DISALLOW_COPY_AND_ASSIGN(LightController);
};

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHT_CONTROLLER__
