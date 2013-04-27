#ifndef __ECHOMESH_LIGHTING_WINDOW__
#define __ECHOMESH_LIGHTING_WINDOW__

#include "echomesh/base/LightConfig.h"
#include "echomesh/component/InstrumentGrid.h"

namespace echomesh {

class LightingWindow : public DocumentWindow {
 public:
  LightingWindow()  : DocumentWindow("echomesh lighting simulator",
                                     Colours::lightgrey,
                                     DocumentWindow::allButtons),
                      instrumentGrid_(new echomesh::InstrumentGrid) {
    setContentOwned(instrumentGrid_, true);
    centreWithSize(getWidth(), getHeight());
    setVisible(true);
    setUsingNativeTitleBar(true);
  }

  void setLights(const ColorList& cl) {
    instrumentGrid_->setLights(cl);
  }

  void setConfig(const LightConfig& config) {
    instrumentGrid_->setConfig(config);
  }

  void closeButtonPressed() {
    // TODO: Send a quit back to the original program.
  }

 private:
  echomesh::InstrumentGrid* instrumentGrid_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(LightingWindow)
};

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHTING_WINDOW__
