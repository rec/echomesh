#ifndef __ECHOMESH_INSTRUMENT_PANEL__
#define __ECHOMESH_INSTRUMENT_PANEL__

#include "echomesh/base/Echomesh.h"
#include "echomesh/base/LightConfig.h"
#include "echomesh/component/Instrument.h"
#include "rec/util/STL.h"

namespace echomesh {

class InstrumentGrid : public Component {
 public:
  InstrumentGrid() {}

  ~InstrumentGrid() { rec::stl::deletePointers(&instruments_); }

  void setConfig(const LightConfig& config) {
    MessageManagerLock l;
    config_ = config;
    int oldCount = instruments_.size();

    for (int i = config_.count; i < oldCount; ++i)
      delete instruments_[i];
    instruments_.resize(config_.count);
    for (int i = oldCount; i < config_.count; ++i)
      instruments_[i] = new Instrument;

    const LightDisplay& light = config_.display.light;
    int delta = light.labelStartsAtZero ? 0 : 1;
    for (int i = 0; i < instruments_.size(); ++i)
      instruments_[i]->configure(String(i + delta), light);

    int top = config_.display.padding.top;
    int left = config_.display.padding.left;
    int columns = config.display.layout.x;
    int rows = config.display.layout.y;

    int w = light.size.x;
    int h = light.size.y;
    int index = 0;
    for (int y = 0; y < rows; ++y) {
      for (int x = 0; x < columns; ++x)
        instruments_[index++]->setBounds(left + x * w, top + y * h, w, h);
    }

    setSize(left + w * columns + config_.display.padding.right,
            top + h * rows + config_.display.padding.bottom);
    repaint();
  }

  void setLights(const ColorList& lights) {
    for (int i = 0; i < lights.size(); ++i)
      instruments_[i]->setColor(lights[i]);
  }

  void paint(Graphics& g) {
    g.fillAll(config_.display.background);
  }

 private:
  LightConfig config_;
  vector<Instrument*> instruments_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(InstrumentGrid)
};

}  // namespace echomesh

#endif  // __ECHOMESH_INSTRUMENT_PANEL__
