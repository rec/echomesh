#ifndef __ECHOMESH_INSTRUMENT_PANEL__
#define __ECHOMESH_INSTRUMENT_PANEL__

#include "echomesh/base/Echomesh.h"
#include "echomesh/component/InstrumentComponent.h"

namespace echomesh {

struct LightConfig;

class InstrumentGrid : public Component {
 public:
  InstrumentGrid();
  virtual ~InstrumentGrid();

  void setConfig(const LightConfig&);
  void setLights(const ColorList&);
  void setLights(const char*);
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
    repaint();
  }

 private:
  void layout();

  vector<unique_ptr<InstrumentComponent>> instruments_;

  bool isUnclipped_;
  bool labelStartsAtZero_;
  bool showLabel_;
  Colour background_;
  int columns_;
  int rows_;

  Point layout_;
  Point size_;
  Point padding_;
  Point instrumentPadding_;
  Point labelPadding_;

  CriticalSection lock_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(InstrumentGrid)
};

}  // namespace echomesh

#endif  // __ECHOMESH_INSTRUMENT_PANEL__
