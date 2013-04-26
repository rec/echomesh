#ifndef __ECHOMESH_INSTRUMENT__
#define __ECHOMESH_INSTRUMENT__

#include "echomesh/base/Echomesh.h"
#include "echomesh/base/LightConfig.h"

namespace echomesh {

class Instrument : public Component {
 public:
  Instrument();
  ~Instrument() {}

  void configure(const String& label, const LightDisplay&);

  void setColor(uint8 r, uint8 g, uint8 b);

  void setColor(const Colour&);
  virtual void paint(Graphics&);

 private:
  String label_;
  LightDisplay config_;
  Colour color_;
  Colour labelColor_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(Instrument)
};

}  // namespace echomesh

#endif  // __ECHOMESH_INSTRUMENT__
