#include "echomesh/LightConfig.h"

namespace echomesh {

using namespace std;

static bool debug = false;

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

void operator>>(const YAML::Node& node, Border& p) {
  node["color"] >> p.color;
  node["width"] >> p.width;
}

void operator>>(const YAML::Node& node, LightDisplay& p) {
  node["background"] >> p.background;
  node["border"] >> p.border;
  node["padding"] >> p.padding;
  node["shape"] >> p.shape;
  node["size"] >> p.size;
}

void operator>>(const YAML::Node& node, Padding& p) {
  node["top"] >> p.top;
  node["left"] >> p.left;
  node["bottom"] >> p.bottom;
  node["right"] >> p.right;
}

void operator>>(const YAML::Node& node, Display& p) {
  debug = true;
  node["background"] >> p.background;
  debug = false;
  node["layout"] >> p.layout;
  node["padding"] >> p.padding;
  node["light"] >> p.light;
}

void operator>>(const YAML::Node& node, LightConfig& p) {
  node["count"] >> p.count;
  node["rgb_order"] >> p.rgb_order;
  node["display"] >> p.display;
}

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

}  // namespace echomesh
