#ifndef __ECHOMESH_LIGHTING_WINDOW__
#define __ECHOMESH_LIGHTING_WINDOW__

#include "yaml-cpp/yaml.h"
#include "echomesh/base/Config.h"
#include "echomesh/component/InstrumentGrid.h"

namespace echomesh {

class LightingWindow : public DocumentWindow {
 public:
  LightingWindow();

  void setLights(const ColorList& cl);
  void setConfig(const LightConfig& config);
  void closeButtonPressed();

  virtual void moved();

 private:
  echomesh::InstrumentGrid* instrumentGrid_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(LightingWindow)
};

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHTING_WINDOW__
