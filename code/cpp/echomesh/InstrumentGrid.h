#ifndef __ECHOMESH_INSTRUMENT_PANEL__
#define __ECHOMESH_INSTRUMENT_PANEL__

#include "echomesh/Echomesh.h"
#include "echomesh/LightConfig.h"
#include "echomesh/Instrument.h"
#include "rec/util/STL.h"

namespace echomesh {

class InstrumentGrid : public Component {
 public:
  InstrumentGrid(const LightConfig& config) : config_(config) {}
  ~InstrumentGrid() { stl::deletePointers(&instruments); }

  void setConfig(const LightConfig& config) {
    MessageManagerLock l;
    config_ = config;
    int oldCount = instruments_.count();

    for (int i = config_.count; i < oldCount; ++i)
      delete instruments_[i];
    instruments_.resize(config_.count);
    for (int i = old_count; i < config_.count; ++i)
      instruments_[i] = new Instrument;

    int delta = config_.labelStartsAtZero ? 0 : 1;
    const LightDisplay& light = config_.display.light;
    for (int i = 0; i < instruments_.size(); ++i)
      instruments_->configure(String(i + delta), light);

    g.fillAll(config_.display.background);
    int width = light.size.x + light.padding.x;
    int height = light.size.y + light.padding.y;

    int index = 0;
    for (int y = 0; y < config.display.layout.y; ++y) {
      for (int x = 0; x < config.display.layout.x; ++x, ++index)
        instruments_->setBounds(x * width, y * height, width, height);
    }

    repaint();
  }


 private:
  LightConfig config_;
  vector<Instrument*> instruments_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(InstrumentGrid)
};

}  // namespace echomesh

#endif  // __ECHOMESH_INSTRUMENT_PANEL__
