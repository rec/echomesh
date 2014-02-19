#pragma once

#include "echomesh/base/Echomesh.h"
#include "echomesh/component/InstrumentComponent.h"

namespace echomesh { namespace color { class FColorList; }}

namespace echomesh {

struct LightConfig;

class InstrumentGrid : public Component {
 public:
  InstrumentGrid();
  virtual ~InstrumentGrid();

  void setLights(const color::FColorList&);
  void setPaintingIsUnclipped(bool);
  void setLightCount(int);
  int getLightCount() const;
  void setLabelStartsAtZero(bool);
  void setShowLabel(bool);
  void setBackground(const Colour&);
  void setLayout(const Point& layout, const Point& size, const Point& padding,
                 const Point& instrumentPadding, const Point& labelPadding);

  void paint(Graphics&);

  void doRepaint() {
    MessageManagerLock l;
    JUCE_AUTORELEASEPOOL {
      repaint();
    }
  }

 private:
  void layout();
  void doSetLights();

  vector<unique_ptr<InstrumentComponent>> instruments_;

  bool isUnclipped_;
  bool labelStartsAtZero_;
  bool showLabel_;
  Colour background_;

  Point layout_;
  Point size_;
  Point padding_;
  Point instrumentPadding_;
  Point labelPadding_;

  CriticalSection lock_;

  vector<unsigned char> cache_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(InstrumentGrid)
};

}  // namespace echomesh

