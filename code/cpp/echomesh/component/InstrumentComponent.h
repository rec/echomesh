#ifndef __ECHOMESH_INSTRUMENT_COMPONENT__
#define __ECHOMESH_INSTRUMENT_COMPONENT__

#include "echomesh/base/Echomesh.h"
#include "echomesh/base/LightConfig.h"

namespace echomesh {

class InstrumentComponent : public Component {
 public:
  InstrumentComponent();
  ~InstrumentComponent() {}

  void configure(const String& label, const Instrument&);

  void setColor(uint8 r, uint8 g, uint8 b);

  void setColor(const Colour&);
  virtual void paint(Graphics&);

 private:
  void setLabel();

  String label_;
  Instrument config_;
  Colour color_;
  Colour labelColor_;
  CriticalSection lock_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(InstrumentComponent)
};

}  // namespace echomesh

#endif  // __ECHOMESH_INSTRUMENT_COMPONENT__
