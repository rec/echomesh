#pragma once

#include "echomesh/component/InstrumentGrid.h"

namespace echomesh { namespace color { class FColorList; }}

namespace echomesh {

class InstrumentGrid;

class LightingWindow : public DocumentWindow {
  public:
    LightingWindow();
    ~LightingWindow();

    InstrumentGrid* grid() { return instrumentGrid_; }
    void saveSnapshotToFile(const string&);

    void closeButtonPressed() override;
    void moved() override;
    void resized() override;
    void setLights(const color::FColorList&);

  private:
    InstrumentGrid* instrumentGrid_;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(LightingWindow)
};

LightingWindow* makeLightingWindow();
void deleteLightingWindow(LightingWindow*);


}  // namespace echomesh
