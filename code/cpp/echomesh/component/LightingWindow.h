#ifndef __ECHOMESH_LIGHTING_WINDOW__
#define __ECHOMESH_LIGHTING_WINDOW__

#include "yaml-cpp/yaml.h"
#include "echomesh/component/InstrumentGrid.h"

namespace echomesh {

class InstrumentGrid;

class LightingWindow : public DocumentWindow {
 public:
  LightingWindow();
  ~LightingWindow();

  void setLights(const ColorList& cl) { grid()->setLights(cl); }
  void closeButtonPressed();
  InstrumentGrid* grid() { return instrumentGrid_; }

  virtual void moved();

 private:
  InstrumentGrid* instrumentGrid_;
  bool runningInTest_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(LightingWindow)
};

LightingWindow* makeLightingWindow();
void deleteLightingWindow(LightingWindow*);


}  // namespace echomesh

#endif  // __ECHOMESH_LIGHTING_WINDOW__
