#ifndef __LIGHT_CONFIG__
#define __LIGHT_CONFIG__

#include "yaml-cpp/yaml.h"

#include "Echomesh.h"

namespace echomesh {
namespace config {

struct Point {
  int x_;
  int y_;
};

struct Border {
  Colour color_;
  int width_;
};

struct LightDisplay {
  Colour background_;
  Border border_;
  string shape_;
  Point size_;
};

struct Padding {
  int top_;
  int left_;
  int bottom_;
  int right_;
  Point light_;
};

struct Display {
  Colour background_;
  Point layout_;
  Padding padding_;
  LightDisplay light_;
};

struct Light {
  int count_;
  string order_;

  Display display_;
};

typedef uint8 ColorComponents[3];

typedef std::vector<Colour> ColorList;

inline void operator>>(const YAML::Node& node, Colour& p) {
  if (node.size()) {
    uint8 r, g, b;
    node[0] >> r;
    node[1] >> b;
    node[2] >> b;
    p = Colour(r, g, b);

  } else {
    uint32 c;
    node >> c;
    p = Colour(c);
  }
}

inline void operator>>(const YAML::Node& node, Point& p) {
  node[0] >> p.x_;
  node[1] >> p.y_;
}

inline void operator>>(const YAML::Node& node, Border& p) {
  node["color"] >> p.color_;
  node["width"] >> p.width_;
}

inline void operator>>(const YAML::Node& node, LightDisplay& p) {
  node["background"] >> p.background_;
  node["border"] >> p.border_;
  node["shape"] >> p.shape_;
  node["size"] >> p.size_;
}

inline void operator>>(const YAML::Node& node, Padding& p) {
  node["top"] >> p.top_;
  node["left"] >> p.left_;
  node["bottom"] >> p.bottom_;
  node["right"] >> p.right_;
  node["light"] >> p.light_;
}

inline void operator>>(const YAML::Node& node, Display& p) {
  node["background"] >> p.background_;
  node["layout"] >> p.layout_;
  node["padding"] >> p.padding_;
  node["light"] >> p.light_;
}

inline void operator>>(const YAML::Node& node, Light& p) {
  node["count"] >> p.count_;
  node["order"] >> p.order_;
  node["display"] >> p.display_;
}

inline void operator>>(const YAML::Node& node, ColorComponents& p) {
  node[0] >> p[0];
  node[1] >> p[1];
  node[2] >> p[2];
}

inline void operator>>(const YAML::Node& node, ColorList& p) {
  for (YAML::Iterator i = node.begin(); i != node.end(); ++i) {
    Colour c;
    *i >> c;
    p.push_back(c);
  }
}

}  // namespace config
}  // namespace echomesh

#endif  // __LIGHT_CONFIG__
