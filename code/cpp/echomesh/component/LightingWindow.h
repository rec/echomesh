#ifndef __ECHOMESH_LIGHTING_WINDOW__
#define __ECHOMESH_LIGHTING_WINDOW__

#include "echomesh/base/LightConfig.h"
#include "echomesh/component/LightComponent.h"
#include "echomesh/component/InstrumentGrid.h"

namespace echomesh {

static const bool USE_INSTRUMENT_GRID = not false;

class LightingWindow : public DocumentWindow {
 public:
  LightingWindow()  : DocumentWindow("echomesh lighting simulator",
                                     Colours::lightgrey,
                                     DocumentWindow::allButtons) {
    if (USE_INSTRUMENT_GRID) {
      instrumentGrid_ = new echomesh::InstrumentGrid();
      lightComponent_ = NULL;
      setContentOwned(instrumentGrid_, true);
    } else {
      instrumentGrid_ = NULL;
      lightComponent_ = new echomesh::LightComponent(this);
      setContentOwned(lightComponent_, true);
    }

    centreWithSize(getWidth(), getHeight());
    setVisible(true);
    setUsingNativeTitleBar(true);
  }

  void setLights(const ColorList& cl) {
    if (lightComponent_)
      lightComponent_->setLights(cl);
    else
      instrumentGrid_->setLights(cl);
  }

  void setConfig(const LightConfig& config) {
    if (lightComponent_)
      lightComponent_->setConfig(config);
    else
      instrumentGrid_->setConfig(config);
  }

  void closeButtonPressed() {
    // TODO: Send a quit back to the original program.
  }

 private:
  echomesh::LightComponent* lightComponent_;
  echomesh::InstrumentGrid* instrumentGrid_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(LightingWindow)
};

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHTING_WINDOW__
