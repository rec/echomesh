#ifndef __LIGHT_COMPONENT__
#define __LIGHT_COMPONENT__

#include "Echomesh.h"
#include "LightConfig.h"

namespace echomesh {

class LightComponent : public Component {
 public:
  LightComponent(DocumentWindow*);
  ~LightComponent() {}

  void paint(Graphics& g);

  void setLights(const ColorList&);
  void setConfig(const LightConfig&);

 private:
  ColorList colors_;
  LightConfig config_;
  bool configEmpty_;
  bool lightsEmpty_;
  DocumentWindow* window_;
  Point boxSize_;

  const Display& display() const { return config_.display; }
  const LightDisplay& light() const { return display().light; }
  const Padding& padding() const { return display().padding; }
  const Point& layout() const { return display().layout; }

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (LightComponent)
};

}  // namespace echomesh

#endif  // __LIGHT_COMPONENT__
