#ifndef __ECHOMESH_INSTRUMENT_PANEL__
#define __ECHOMESH_INSTRUMENT_PANEL__

#include "echomesh/base/Echomesh.h"
#include "echomesh/component/InstrumentComponent.h"

namespace echomesh {

class LightConfig;

class InstrumentGrid : public Component {
 public:
  InstrumentGrid();
  virtual ~InstrumentGrid();

  void setConfig(const LightConfig&);
  void setLights(const ColorList&);
  void paint(Graphics&);
  void setPaintingIsUnclipped(bool);
  void setLightCount(int);
  void setLabelStartsAtZero(bool);
  void setBackground(const Colour&);
  void setLayout(const Point& layout, const Point& size, const Point& padding,
                 const Point& instrumentPadding, const Point& labelPadding);

 private:
  void layout();

  vector<unique_ptr<InstrumentComponent>> instruments_;

  bool isUnclipped_;
  bool labelStartsAtZero_;
  CriticalSection lock_;
  Colour background_;
  int columns_;
  int rows_;

  Point layout_;
  Point size_;
  Point padding_;
  Point instrumentPadding_;
  Point labelPadding_;

  JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(InstrumentGrid)
};

}  // namespace echomesh

#endif  // __ECHOMESH_INSTRUMENT_PANEL__
