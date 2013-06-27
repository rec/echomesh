#include "echomesh/base/Config.h"

namespace echomesh {

using namespace std;

void operator>>(const YAML::Node& node, ColorBytes& p) {
  node[0] >> p[0];
  node[1] >> p[1];
  node[2] >> p[2];
}

void operator>>(const YAML::Node& node, ColorList& p) {
  p.resize(node.size());

  for (int i = 0; i < node.size(); ++i)
    node[i] >> p[i];
}

void operator>>(const YAML::Node& node, Colour& p) {
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

void operator>>(const YAML::Node& node, Point& p) {
  if (const YAML::Node *pName = node.FindValue("x")) {
    *pName >> p.x;
    node["y"] >> p.y;
  } else {
    node[0] >> p.x;
    node[1] >> p.y;
  }
}

void operator>>(const YAML::Node& node, SampleTime& t) {
  uint64 time;
  node >> time;
  t = time;
}

void operator>>(const YAML::Node& node, RealTime& t) {
  double time;
  node >> time;
  t = time;
}


void operator>>(const YAML::Node& node, Border& p) {
  node["color"] >> p.color;
  node["width"] >> p.width;
}

void operator>>(const YAML::Node& node, Instrument& p) {
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

void operator>>(const YAML::Node& node, Visualizer& p) {
  node["background"] >> p.background;
  node["instrument"] >> p.instrument;
  node["layout"] >> p.layout;
  node["padding"] >> p.padding;
  node["period"] >> p.period;
  node["show"] >> p.show;
  node["top_left"] >> p.topLeft;
}

void operator>>(const YAML::Node& node, Hardware& p) {
  node["enable"] >> p.enable;
  node["period"] >> p.period;
  node["local"] >> p.local;
  node["rgb_order"] >> p.rgbOrder;
}

void operator>>(const YAML::Node& node, OneMidiConfig& p) {
  node["external"] >> p.external;
  node["index"] >> p.index;
  node["name"] >> p.name;
}

void operator>>(const YAML::Node& node, MidiConfig& p) {
  node["input"] >> p.input;
  node["output"] >> p.output;
}

void operator>>(const YAML::Node& node, LightConfig& p) {
  node["count"] >> p.count;
  node["enable"] >> p.enable;
  node["hardware"] >> p.hardware;
  node["visualizer"] >> p.visualizer;
}

void operator>>(const YAML::Node& node, Config& p) {
  node["light"] >> p.light;
  node["midi"] >> p.midi;
}

}  // namespace echomesh
