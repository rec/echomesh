#ifndef __ECHOMESH_LIGHTING_WINDOW__
#define __ECHOMESH_LIGHTING_WINDOW__

#include "echomesh/component/LightComponent.h"

namespace echomesh {

class LightingWindow : public DocumentWindow {
 public:
  LightingWindow()  : DocumentWindow("echomesh lighting simulator",
                                     Colours::lightgrey,
                                     DocumentWindow::allButtons) {
    comp_ = new echomesh::LightComponent(this);
    setContentOwned(comp_, true);

    centreWithSize(getWidth(), getHeight());
    setVisible(true);
    setUsingNativeTitleBar(true);
  }

  void closeButtonPressed() {
    // TODO: Send a quit back to the original program.
  }

  echomesh::LightComponent* comp_;

 private:
  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(LightingWindow)
};

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHTING_WINDOW__
