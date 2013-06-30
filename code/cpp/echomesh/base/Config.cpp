#include <limits>

#include "echomesh/base/Config.h"

namespace echomesh {

using namespace std;

static SampleRate SAMPLE_RATE(44100.0);

void operator>>(const Node& node, ColorBytes& p) {
  node[0] >> p[0];
  node[1] >> p[1];
  node[2] >> p[2];
}

void operator>>(const Node& node, Colour& p) {
  if (node.size()) {
    float r, g, b;
    node[0] >> r;
    node[1] >> g;
    node[2] >> b;

    p = Colour::fromFloatRGBA(r, g, b, 1.0f);
  } else {
    uint32 c;
    node >> c;
    p = Colour(c);
  }
}

void operator>>(const Node& node, Point& p) {
  if (const Node *pName = node.FindValue("x")) {
    *pName >> p.x;
    node["y"] >> p.y;
  } else {
    node[0] >> p.x;
    node[1] >> p.y;
  }
}

void operator>>(const Node& node, SampleTime& t) {
  double time;
  node >> time;
  if (isinf(time)) {
    t = (time > 0.0) ? numeric_limits<int64>::max() :
      numeric_limits<int64>::min();
  } else {
    t = SampleTime(time, SAMPLE_RATE);
  }
}

void operator>>(const Node& node, RealTime& t) {
  double time;
  node >> time;
  t = time;
}


void operator>>(const Node& node, Border& p) {
  node["color"] >> p.color;
  node["width"] >> p.width;
}

void operator>>(const Node& node, Instrument& p) {
  node["background"] >> p.background;
  node["border"] >> p.border;
  node["label"] >> p.label;
  node["label_padding"] >> p.labelPadding;
  node["label_starts_at_zero"] >> p.labelStartsAtZero;
  node["padding"] >> p.padding;
  node["paint_unclipped"] >> p.paintUnclipped;
  node["shape"] >> p.shape;
  node["size"] >> p.size;
  p.isRect = not string("rectangle").find(p.shape);
}

void operator>>(const Node& node, Visualizer& p) {
  node["background"] >> p.background;
  node["instrument"] >> p.instrument;
  node["layout"] >> p.layout;
  node["padding"] >> p.padding;
  node["period"] >> p.period;
  node["show"] >> p.show;
  node["top_left"] >> p.topLeft;
}

void operator>>(const Node& node, Hardware& p) {
  node["enable"] >> p.enable;
  node["period"] >> p.period;
  node["local"] >> p.local;
  node["rgb_order"] >> p.rgbOrder;
}

void operator>>(const Node& node, OneMidiConfig& p) {
  node["external"] >> p.external;
  node["index"] >> p.index;
  node["name"] >> p.name;
}

void operator>>(const Node& node, MidiConfig& p) {
  node["input"] >> p.input;
  node["output"] >> p.output;
}

void operator>>(const Node& node, LightConfig& p) {
  node["count"] >> p.count;
  node["enable"] >> p.enable;
  node["hardware"] >> p.hardware;
  node["visualizer"] >> p.visualizer;
}

void operator>>(const Node& node, Config& p) {
  node["light"] >> p.light;
  node["midi"] >> p.midi;
}

}  // namespace echomesh
