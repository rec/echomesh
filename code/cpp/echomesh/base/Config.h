#ifndef __ECHOMESH_LIGHT_CONFIG__
#define __ECHOMESH_LIGHT_CONFIG__

#include "yaml-cpp/yaml.h"

#include "echomesh/base/Echomesh.h"

namespace echomesh {

// See echomesh/code/python/echomesh/config/config.yml

struct Point {
  Point() {}
  Point(int x_, int y_) : x(x_), y(y_) {}
  int x;
  int y;
};

struct Border {
  Colour color;
  int width;
};

struct Instrument {
  Colour background;
  Border border;
  bool isRect;
  bool label;
  Point labelPadding;
  bool labelStartsAtZero;
  Point padding;
  bool paintUnclipped;
  Point size;
  string shape;
};

struct Visualizer {
  Colour background;
  Instrument instrument;
  Point layout;
  Point padding;
  Point topLeft;
  SampleTime period;
  bool show;
};

struct Hardware {
  bool enable;
  SampleTime period;
  bool local;
  string rgbOrder;
};

struct LightConfig {
  int count;
  bool enable;
  Hardware hardware;

  Visualizer visualizer;
};

struct OneMidiConfig {
  bool external;
  int index;
  string name;
};

struct MidiConfig {
  OneMidiConfig input, output;
};

struct Config {
  LightConfig light;
  MidiConfig midi;
};

typedef uint8 ColorBytes[3];
typedef std::vector<Colour> ColorList;
typedef std::vector<uint8> ByteList;

template <typename Array>
void fillArray(const Node& node, Array* array) {
  array->resize(node.size());

  for (int i = 0; i < node.size(); ++i)
    node[i] >> (*array)[i];
}

template <typename T>
inline void operator>>(const Node& n, vector<T>& vt) { fillArray(n, &vt); }

void operator>>(const Node&, ColorBytes&);
void operator>>(const Node&, Colour&);
void operator>>(const Node&, Point&);
void operator>>(const Node&, Border&);
void operator>>(const Node&, Instrument&);
void operator>>(const Node&, Visualizer&);
void operator>>(const Node&, Hardware&);
void operator>>(const Node&, OneMidiConfig&);
void operator>>(const Node&, MidiConfig&);
void operator>>(const Node&, LightConfig&);
void operator>>(const Node&, Config&);
void operator>>(const Node&, SampleTime&);
void operator>>(const Node&, RealTime&);

}  // namespace echomesh

#endif  // __ECHOMESH_LIGHT_CONFIG__
