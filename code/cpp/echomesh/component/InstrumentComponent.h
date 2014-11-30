#pragma once

#include "echomesh/base/Echomesh.h"

namespace echomesh {

class InstrumentComponent : public Component {
 public:
  InstrumentComponent();
  ~InstrumentComponent() {}

  void setColor(const Colour&);
  virtual void paint(Graphics&);
  void setShape(bool isRect);
  void setLabelPadding(int x, int y);
  void setShowLabel(bool show);
  void setLabel(const String&);

 private:
  String label_;
  Colour color_;
  Colour labelColor_;
  CriticalSection lock_;

  bool isRect_;
  int labelPaddingX_;
  int labelPaddingY_;
  bool showLabel_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(InstrumentComponent)
};

}  // namespace echomesh
