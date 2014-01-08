#include <map>

#include "echomesh/color/ColorName.h"
#include "echomesh/color/FColor.h"
#include "echomesh/color/FColorList.h"

using namespace std;

namespace echomesh {
namespace color {

namespace {

int compareColours(const Colour& x, const Colour& y) {
  auto xa = x.getARGB();
  auto ya = y.getARGB();
  auto xrgb = xa & 0xffffff;
  auto yrgb = ya & 0xffffff;
  if (xrgb < yrgb)
    return -1;
  if (xrgb > yrgb)
    return 1;
  if (xa < ya)
    return -1;
  if (xa > ya)
    return 1;
  return 0;
}

struct Compare {
  bool operator()(const Colour& x, const Colour& y) const {
    return compareColours(x, y) < 0;
  }
};

struct ColorNamer {
  std::map<String, Colour> stringToColor_;
  std::map<Colour, String, Compare> colorToString_;

  void add(const String& s, uint32 h) {
    add(s, Colour(h));
  }

  void add(const String& s, const Colour& c) {
    stringToColor_[s.replace(" ", "")] = c;
    colorToString_[c] = s;
  }
};

ColorNamer makeNamer() {
  ColorNamer namer;

  namer.add("alice blue", 0xfff0f8ff);
  namer.add("antique white", 0xfffaebd7);
  namer.add("aqua", 0xff00ffff);
  namer.add("aquamarine", 0xff7fffd4);
  namer.add("azure", 0xfff0ffff);
  namer.add("beige", 0xfff5f5dc);
  namer.add("bisque", 0xffffe4c4);
  namer.add("black", 0xff000000);
  namer.add("blanched almond", 0xffffebcd);
  namer.add("blue", 0xff0000ff);
  namer.add("blue violet", 0xff8a2be2);
  namer.add("brown", 0xffa52a2a);
  namer.add("burly wood", 0xffdeb887);
  namer.add("cadet blue", 0xff5f9ea0);
  namer.add("chartreuse", 0xff7fff00);
  namer.add("chocolate", 0xffd2691e);
  namer.add("coral", 0xffff7f50);
  namer.add("cornflower blue", 0xff6495ed);
  namer.add("corn silk", 0xfffff8dc);
  namer.add("crimson", 0xffdc143c);
  namer.add("cyan", 0xff00ffff);
  namer.add("dark blue", 0xff00008b);
  namer.add("dark cyan", 0xff008b8b);
  namer.add("dark goldenrod", 0xffb8860b);
  namer.add("dark green", 0xff006400);
  namer.add("dark grey", 0xff555555);
  namer.add("dark khaki", 0xffbdb76b);
  namer.add("dark magenta", 0xff8b008b);
  namer.add("dark olive green", 0xff556b2f);
  namer.add("dark orange", 0xffff8c00);
  namer.add("dark orchid", 0xff9932cc);
  namer.add("dark red", 0xff8b0000);
  namer.add("dark salmon", 0xffe9967a);
  namer.add("dark sea green", 0xff8fbc8f);
  namer.add("dark slate blue", 0xff483d8b);
  namer.add("dark slate grey", 0xff2f4f4f);
  namer.add("dark turquoise", 0xff00ced1);
  namer.add("dark violet", 0xff9400d3);
  namer.add("deep pink", 0xffff1493);
  namer.add("deep sky blue", 0xff00bfff);
  namer.add("dim grey", 0xff696969);
  namer.add("dodger blue", 0xff1e90ff);
  namer.add("fire brick", 0xffb22222);
  namer.add("floral white", 0xfffffaf0);
  namer.add("forest green", 0xff228b22);
  namer.add("fuchsia", 0xffff00ff);
  namer.add("gainsboro", 0xffdcdcdc);
  namer.add("gold", 0xffffd700);
  namer.add("goldenrod", 0xffdaa520);
  namer.add("green", 0xff00ff00);
  namer.add("green yellow", 0xffadff2f);
  namer.add("grey", 0xff808080);
  namer.add("honeydew", 0xfff0fff0);
  namer.add("hot pink", 0xffff69b4);
  namer.add("indian red", 0xffcd5c5c);
  namer.add("indigo", 0xff4b0082);
  namer.add("ivory", 0xfffffff0);
  namer.add("khaki", 0xfff0e68c);
  namer.add("lavender", 0xffe6e6fa);
  namer.add("lavender blush", 0xfffff0f5);
  namer.add("lemon chiffon", 0xfffffacd);
  namer.add("light blue", 0xffadd8e6);
  namer.add("light coral", 0xfff08080);
  namer.add("light cyan", 0xffe0ffff);
  namer.add("light goldenrod yellow", 0xfffafad2);
  namer.add("light green", 0xff90ee90);
  namer.add("light grey", 0xffd3d3d3);
  namer.add("light pink", 0xffffb6c1);
  namer.add("light salmon", 0xffffa07a);
  namer.add("light sea green", 0xff20b2aa);
  namer.add("light sky blue", 0xff87cefa);
  namer.add("light slate grey", 0xff778899);
  namer.add("light steel blue", 0xffb0c4de);
  namer.add("light yellow", 0xffffffe0);
  namer.add("limegreen", 0xff32cd32);
  namer.add("linen", 0xfffaf0e6);
  namer.add("magenta", 0xffff00ff);
  namer.add("maroon", 0xff800000);
  namer.add("medium aquamarine", 0xff66cdaa);
  namer.add("medium blue", 0xff0000cd);
  namer.add("medium orchid", 0xffba55d3);
  namer.add("medium purple", 0xff9370db);
  namer.add("medium seagreen", 0xff3cb371);
  namer.add("medium slateblue", 0xff7b68ee);
  namer.add("medium springgreen", 0xff00fa9a);
  namer.add("medium turquoise", 0xff48d1cc);
  namer.add("medium violet red", 0xffc71585);
  namer.add("midnight blue", 0xff191970);
  namer.add("mint cream", 0xfff5fffa);
  namer.add("misty rose", 0xffffe4e1);
  namer.add("navajo white", 0xffffdead);
  namer.add("navy", 0xff000080);
  namer.add("none", 0x00000000);
  namer.add("old lace", 0xfffdf5e6);
  namer.add("olive", 0xff808000);
  namer.add("olive drab", 0xff6b8e23);
  namer.add("orange", 0xffffa500);
  namer.add("orange red", 0xffff4500);
  namer.add("orchid", 0xffda70d6);
  namer.add("pale goldenrod", 0xffeee8aa);
  namer.add("pale green", 0xff98fb98);
  namer.add("pale turquoise", 0xffafeeee);
  namer.add("pale violet red", 0xffdb7093);
  namer.add("papaya whip", 0xffffefd5);
  namer.add("peachpuff", 0xffffdab9);
  namer.add("peru", 0xffcd853f);
  namer.add("pink", 0xffffc0cb);
  namer.add("plum", 0xffdda0dd);
  namer.add("powder blue", 0xffb0e0e6);
  namer.add("purple", 0xff800080);
  namer.add("red", 0xffff0000);
  namer.add("rosy brown", 0xffbc8f8f);
  namer.add("royal blue", 0xff4169e1);
  namer.add("saddle brown", 0xff8b4513);
  namer.add("salmon", 0xfffa8072);
  namer.add("sandy brown", 0xfff4a460);
  namer.add("sea green", 0xff2e8b57);
  namer.add("seashell", 0xfffff5ee);
  namer.add("sienna", 0xffa0522d);
  namer.add("silver", 0xffc0c0c0);
  namer.add("sky blue", 0xff87ceeb);
  namer.add("slate blue", 0xff6a5acd);
  namer.add("slate grey", 0xff708090);
  namer.add("snow", 0xfffffafa);
  namer.add("springgreen", 0xff00ff7f);
  namer.add("steel blue", 0xff4682b4);
  namer.add("tan", 0xffd2b48c);
  namer.add("teal", 0xff008080);
  namer.add("thistle", 0xffd8bfd8);
  namer.add("tomato", 0xffff6347);
  namer.add("turquoise", 0xff40e0d0);
  namer.add("violet", 0xffee82ee);
  namer.add("wheat", 0xfff5deb3);
  namer.add("white", 0xffffffff);
  namer.add("white smoke", 0xfff5f5f5);
  namer.add("yellow", 0xffffff00);
  namer.add("yellow green", 0xff9acd32);

  for (auto i = 1; i < 100; ++i) {
    auto g = (i * 255) / 100;
    namer.add("grey " + String(i), Colour(g, g, g));
  }

  return namer;
}

static const ColorNamer NAMER = makeNamer();

} // namespace

bool nameToRgb(const String& cname, FColor* color) {
  auto name = cname.trim().toLowerCase().
      replace("gray", "grey").replace(" ", "");
  if (name.isEmpty())
    return false;

  if (name[0] == '#' or name.containsOnly("abcdef0123456789")) {
    *color = FColor((uint32) name.getHexValue32());
    return true;
  }

  auto i = NAMER.stringToColor_.find(name);
  auto success = (i != NAMER.stringToColor_.end());
  if (success)
    *color = FColor(i->second);
  return success;
}

string rgbToName(const FColor& fcolor) {
  Colour color = fcolor.toColour();
  if (not color.getARGB())
    return "none";
  String suffix;
  FColor c;
  if (color.isOpaque()) {
    c = color;
  } else {
    c = color.withAlpha(1.0f);
    suffix = ", alpha=" + String(fcolor.alpha(), 3) + "]";
  }
  auto i = NAMER.colorToString_.find(c.toColour());
  String name;
  if (i != NAMER.colorToString_.end()) {
    name = i->second;
    if (not suffix.isEmpty())
      name = "[" + name;
  } else {
    name = "[red=" + String(fcolor.red(), 3) +
        ", green=" + String(fcolor.green(), 3) +
        ", blue=" + String(fcolor.blue(), 3);
    if (suffix.isEmpty())
      suffix += "]";
  }
  return (name + suffix).toStdString();
}

}  // namespace color
}  // namespace echomesh
