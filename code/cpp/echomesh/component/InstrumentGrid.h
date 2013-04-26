#ifndef __ECHOMESH_INSTRUMENT_PANEL__
#define __ECHOMESH_INSTRUMENT_PANEL__

#include "echomesh/base/Echomesh.h"
#include "echomesh/base/LightConfig.h"
#include "echomesh/component/Instrument.h"

namespace echomesh {

class InstrumentGrid : public Component {
 public:
  InstrumentGrid();
  virtual ~InstrumentGrid();

  void setConfig(const LightConfig&);
  void setLights(const ColorList&);
  void paint(Graphics&);

 private:
  LightConfig config_;
  vector<Instrument*> instruments_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(InstrumentGrid)
};

}  // namespace echomesh

#endif  // __ECHOMESH_INSTRUMENT_PANEL__
