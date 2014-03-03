#include <map>
#include <tuple>

#include "echomesh/color/ColorName.h"
#include "echomesh/color/FColor.h"
#include "echomesh/color/FColorList.h"

using namespace std;

namespace echomesh {
namespace color {

namespace {

string replace(string subject, const string& search, const string& replace) {
  size_t pos = 0;
  while ((pos = subject.find(search, pos)) != string::npos) {
    subject.replace(pos, search.length(), replace);
    pos += replace.length();
  }
  return subject;
}

void lower(string* subject) {
  for (auto& ch: *subject)
    ch = tolower(ch);
}

// Return a float as "x.xxx".
string toString(float f) {
  f = min(1.0f, max(0.0f, f));
  string result;
  result.resize(5);
  result.resize(sprintf(&result.front(), "%.3f", f));
  return result;
}

// Return a float as "xx.x or 100.0".
string toPercent(float g) {
  auto f = roundf(min(1.0f, max(0.0f, g)) * 1000.0f) / 10.0f;
  string result;
  result.resize(5);
  result.resize(sprintf(&result.front(), "%.1f", f));
  if (result.find(".0") != string::npos)
    result = result.substr(0, result.size() - 2);
  return result;
}

bool isHex(const string& s) {
  return strspn(s.data(), "abcdef0123456789") == s.size();
}

uint32 fromHex(const char* s) {
  uint32 decimalValue;
  sscanf(s, "%u", &decimalValue);
  return decimalValue;
}

struct ColorNamer {
  map<string, FColor> stringToColor_;
  map<FColor, string> colorToString_;

  void add(const string& s, uint32 argb) {
    FColor c(argb);
    stringToColor_[replace(s, " ", "")] = c;
    if (colorToString_.find(c) == colorToString_.end())
      colorToString_[c] = s;
  }
};

ColorNamer makeNamer() {
  ColorNamer namer;

  namer.add("cyan", 0xff00ffff);
  namer.add("dark blue", 0xff00008b);
  namer.add("dark cyan", 0xff008b8b);
  namer.add("magenta", 0xffff00ff);
  namer.add("medium aquamarine", 0xff66cdaa);
  namer.add("medium blue", 0xff0000cd);
  namer.add("yellow green", 0xff9acd32);

  namer.add("alice blue", 0xfff0f8ff);
  namer.add("antique white", 0xfffaebd7);
  namer.add("antique white 1", 0xffffefdb);
  namer.add("antique white 2", 0xffeedfcc);
  namer.add("antique white 3", 0xffcdc0b0);
  namer.add("antique white 4", 0xff8b8378);
  namer.add("aqua", 0xff00ffff);
  namer.add("aquamarine", 0xff7fffd4);
  namer.add("aquamarine 1", 0xff7fffd4);
  namer.add("aquamarine 2", 0xff76eec6);
  namer.add("aquamarine 3", 0xff66cdaa);
  namer.add("aquamarine 4", 0xff458b74);
  namer.add("azure", 0xfff0ffff);
  namer.add("azure 1", 0xfff0ffff);
  namer.add("azure 2", 0xffe0eeee);
  namer.add("azure 3", 0xffc1cdcd);
  namer.add("azure 4", 0xff838b8b);
  namer.add("banana", 0xffe3cf57);
  namer.add("beige", 0xfff5f5dc);
  namer.add("bisque", 0xffffe4c4);
  namer.add("bisque 1", 0xffffe4c4);
  namer.add("bisque 2", 0xffeed5b7);
  namer.add("bisque 3", 0xffcdb79e);
  namer.add("bisque 4", 0xff8b7d6b);
  namer.add("black", 0xff000000);
  namer.add("blanched almond", 0xffffebcd);
  namer.add("blue", 0xff0000ff);
  namer.add("blue 2", 0xff0000ee);
  namer.add("blue 3", 0xff0000cd);
  namer.add("blue 4", 0xff00008b);
  namer.add("blue violet", 0xff8a2be2);
  namer.add("brick", 0xff9c661f);
  namer.add("brown", 0xffa52a2a);
  namer.add("brown 1", 0xffff4040);
  namer.add("brown 2", 0xffee3b3b);
  namer.add("brown 3", 0xffcd3333);
  namer.add("brown 4", 0xff8b2323);
  namer.add("burly wood", 0xffdeb887);
  namer.add("burly wood 1", 0xffffd39b);
  namer.add("burly wood 2", 0xffeec591);
  namer.add("burly wood 3", 0xffcdaa7d);
  namer.add("burly wood 4", 0xff8b7355);
  namer.add("burnt sienna", 0xff8a360f);
  namer.add("burnt umber", 0xff8a3324);
  namer.add("cadet blue", 0xff5f9ea0);
  namer.add("cadet blue 1", 0xff98f5ff);
  namer.add("cadet blue 2", 0xff8ee5ee);
  namer.add("cadet blue 3", 0xff7ac5cd);
  namer.add("cadet blue 4", 0xff53868b);
  namer.add("cadmium orange", 0xffff6103);
  namer.add("cadmium yellow", 0xffff9912);
  namer.add("carrot", 0xffed9121);
  namer.add("chartreuse", 0xff7fff00);
  namer.add("chartreuse 1", 0xff7fff00);
  namer.add("chartreuse 2", 0xff76ee00);
  namer.add("chartreuse 3", 0xff66cd00);
  namer.add("chartreuse 4", 0xff458b00);
  namer.add("chocolate", 0xffd2691e);
  namer.add("chocolate 1", 0xffff7f24);
  namer.add("chocolate 2", 0xffee7621);
  namer.add("chocolate 3", 0xffcd661d);
  namer.add("chocolate 4", 0xff8b4513);
  namer.add("cobalt", 0xff3d59ab);
  namer.add("cobalt green", 0xff3d9140);
  namer.add("cold grey", 0xff808a87);
  namer.add("coral", 0xffff7f50);
  namer.add("coral 1", 0xffff7256);
  namer.add("coral 2", 0xffee6a50);
  namer.add("coral 3", 0xffcd5b45);
  namer.add("coral 4", 0xff8b3e2f);
  namer.add("corn silk", 0xfffff8dc);
  namer.add("corn silk 1", 0xfffff8dc);
  namer.add("corn silk 2", 0xffeee8cd);
  namer.add("corn silk 3", 0xffcdc8b1);
  namer.add("corn silk 4", 0xff8b8878);
  namer.add("cornflower blue", 0xff6495ed);
  namer.add("crimson", 0xffdc143c);
  namer.add("cyan 2", 0xff00eeee);
  namer.add("cyan 3", 0xff00cdcd);
  namer.add("cyan 4", 0xff008b8b);
  namer.add("dark goldenrod", 0xffb8860b);
  namer.add("dark goldenrod 1", 0xffffb90f);
  namer.add("dark goldenrod 2", 0xffeead0e);
  namer.add("dark goldenrod 3", 0xffcd950c);
  namer.add("dark goldenrod 4", 0xff8b6508);
  namer.add("dark green", 0xff006400);
  namer.add("dark grey", 0xff555555);
  namer.add("dark khaki", 0xffbdb76b);
  namer.add("dark magenta", 0xff8b008b);
  namer.add("dark olive green", 0xff556b2f);
  namer.add("dark olivegreen", 0xff556b2f);
  namer.add("dark olivegreen 1", 0xffcaff70);
  namer.add("dark olivegreen 2", 0xffbcee68);
  namer.add("dark olivegreen 3", 0xffa2cd5a);
  namer.add("dark olivegreen 4", 0xff6e8b3d);
  namer.add("dark orange", 0xffff8c00);
  namer.add("dark orange 1", 0xffff7f00);
  namer.add("dark orange 2", 0xffee7600);
  namer.add("dark orange 3", 0xffcd6600);
  namer.add("dark orange 4", 0xff8b4500);
  namer.add("dark orchid", 0xff9932cc);
  namer.add("dark orchid 1", 0xffbf3eff);
  namer.add("dark orchid 2", 0xffb23aee);
  namer.add("dark orchid 3", 0xff9a32cd);
  namer.add("dark orchid 4", 0xff68228b);
  namer.add("dark red", 0xff8b0000);
  namer.add("dark salmon", 0xffe9967a);
  namer.add("dark sea green", 0xff8fbc8f);
  namer.add("dark sea green 1", 0xffc1ffc1);
  namer.add("dark sea green 2", 0xffb4eeb4);
  namer.add("dark sea green 3", 0xff9bcd9b);
  namer.add("dark sea green 4", 0xff698b69);
  namer.add("dark slate blue", 0xff483d8b);
  namer.add("dark slate grey", 0xff2f4f4f);
  namer.add("dark slate grey 1", 0xff97ffff);
  namer.add("dark slate grey 2", 0xff8deeee);
  namer.add("dark slate grey 3", 0xff79cdcd);
  namer.add("dark slate grey 4", 0xff528b8b);
  namer.add("dark turquoise", 0xff00ced1);
  namer.add("dark violet", 0xff9400d3);
  namer.add("deep pink", 0xffff1493);
  namer.add("deep pink 1", 0xffff1493);
  namer.add("deep pink 2", 0xffee1289);
  namer.add("deep pink 3", 0xffcd1076);
  namer.add("deep pink 4", 0xff8b0a50);
  namer.add("deep sky blue", 0xff00bfff);
  namer.add("deep sky blue 1", 0xff00bfff);
  namer.add("deep sky blue 2", 0xff00b2ee);
  namer.add("deep sky blue 3", 0xff009acd);
  namer.add("deep sky blue 4", 0xff00688b);
  namer.add("dim grey", 0xff696969);
  namer.add("dodger blue", 0xff1e90ff);
  namer.add("dodger blue 1", 0xff1e90ff);
  namer.add("dodger blue 2", 0xff1c86ee);
  namer.add("dodger blue 3", 0xff1874cd);
  namer.add("dodger blue 4", 0xff104e8b);
  namer.add("eggshell", 0xfffce6c9);
  namer.add("emerald green", 0xff00c957);
  namer.add("fire brick", 0xffb22222);
  namer.add("fire brick 1", 0xffff3030);
  namer.add("fire brick 2", 0xffee2c2c);
  namer.add("fire brick 3", 0xffcd2626);
  namer.add("fire brick 4", 0xff8b1a1a);
  namer.add("flesh", 0xffff7d40);
  namer.add("floral white", 0xfffffaf0);
  namer.add("forest green", 0xff228b22);
  namer.add("fuchsia", 0xffff00ff);
  namer.add("gainsboro", 0xffdcdcdc);
  namer.add("ghost white", 0xfff8f8ff);
  namer.add("gold", 0xffffd700);
  namer.add("gold 1", 0xffffd700);
  namer.add("gold 2", 0xffeec900);
  namer.add("gold 3", 0xffcdad00);
  namer.add("gold 4", 0xff8b7500);
  namer.add("goldenrod", 0xffdaa520);
  namer.add("goldenrod 1", 0xffffc125);
  namer.add("goldenrod 2", 0xffeeb422);
  namer.add("goldenrod 3", 0xffcd9b1d);
  namer.add("goldenrod 4", 0xff8b6914);
  namer.add("green", 0xff00ff00);
  namer.add("green 1", 0xff00ff00);
  namer.add("green 2", 0xff00ee00);
  namer.add("green 3", 0xff00cd00);
  namer.add("green 4", 0xff008b00);
  namer.add("green yellow", 0xffadff2f);
  namer.add("grey", 0xff808080);
  namer.add("honeydew", 0xfff0fff0);
  namer.add("honeydew 1", 0xfff0fff0);
  namer.add("honeydew 2", 0xffe0eee0);
  namer.add("honeydew 3", 0xffc1cdc1);
  namer.add("honeydew 4", 0xff838b83);
  namer.add("hot pink", 0xffff69b4);
  namer.add("hot pink 1", 0xffff6eb4);
  namer.add("hot pink 2", 0xffee6aa7);
  namer.add("hot pink 3", 0xffcd6090);
  namer.add("hot pink 4", 0xff8b3a62);
  namer.add("indian red", 0xffcd5c5c);
  namer.add("indian red 1", 0xffff6a6a);
  namer.add("indian red 2", 0xffee6363);
  namer.add("indian red 3", 0xffcd5555);
  namer.add("indian red 4", 0xff8b3a3a);
  namer.add("indigo", 0xff4b0082);
  namer.add("ivory", 0xfffffff0);
  namer.add("ivory 1", 0xfffffff0);
  namer.add("ivory 2", 0xffeeeee0);
  namer.add("ivory 3", 0xffcdcdc1);
  namer.add("ivory 4", 0xff8b8b83);
  namer.add("ivory black", 0xff292421);
  namer.add("khaki", 0xfff0e68c);
  namer.add("khaki 1", 0xfffff68f);
  namer.add("khaki 2", 0xffeee685);
  namer.add("khaki 3", 0xffcdc673);
  namer.add("khaki 4", 0xff8b864e);
  namer.add("lavender", 0xffe6e6fa);
  namer.add("lavender blush", 0xfffff0f5);
  namer.add("lavender blush 1", 0xfffff0f5);
  namer.add("lavender blush 2", 0xffeee0e5);
  namer.add("lavender blush 3", 0xffcdc1c5);
  namer.add("lavender blush 4", 0xff8b8386);
  namer.add("lawn green", 0xff7cfc00);
  namer.add("lemon chiffon", 0xfffffacd);
  namer.add("lemon chiffon 1", 0xfffffacd);
  namer.add("lemon chiffon 2", 0xffeee9bf);
  namer.add("lemon chiffon 3", 0xffcdc9a5);
  namer.add("lemon chiffon 4", 0xff8b8970);
  namer.add("light blue", 0xffadd8e6);
  namer.add("light blue 1", 0xffbfefff);
  namer.add("light blue 2", 0xffb2dfee);
  namer.add("light blue 3", 0xff9ac0cd);
  namer.add("light blue 4", 0xff68838b);
  namer.add("light coral", 0xfff08080);
  namer.add("light cyan", 0xffe0ffff);
  namer.add("light cyan 1", 0xffe0ffff);
  namer.add("light cyan 2", 0xffd1eeee);
  namer.add("light cyan 3", 0xffb4cdcd);
  namer.add("light cyan 4", 0xff7a8b8b);
  namer.add("light goldenrod 1", 0xffffec8b);
  namer.add("light goldenrod 2", 0xffeedc82);
  namer.add("light goldenrod 3", 0xffcdbe70);
  namer.add("light goldenrod 4", 0xff8b814c);
  namer.add("light goldenrod yellow", 0xfffafad2);
  namer.add("light green", 0xff90ee90);
  namer.add("light grey", 0xffd3d3d3);
  namer.add("light pink", 0xffffb6c1);
  namer.add("light pink 1", 0xffffaeb9);
  namer.add("light pink 2", 0xffeea2ad);
  namer.add("light pink 3", 0xffcd8c95);
  namer.add("light pink 4", 0xff8b5f65);
  namer.add("light salmon", 0xffffa07a);
  namer.add("light salmon 1", 0xffffa07a);
  namer.add("light salmon 2", 0xffee9572);
  namer.add("light salmon 3", 0xffcd8162);
  namer.add("light salmon 4", 0xff8b5742);
  namer.add("light sea green", 0xff20b2aa);
  namer.add("light sky blue", 0xff87cefa);
  namer.add("light sky blue 1", 0xffb0e2ff);
  namer.add("light sky blue 2", 0xffa4d3ee);
  namer.add("light sky blue 3", 0xff8db6cd);
  namer.add("light sky blue 4", 0xff607b8b);
  namer.add("light slate blue", 0xff8470ff);
  namer.add("light slate grey", 0xff778899);
  namer.add("light steel blue", 0xffb0c4de);
  namer.add("light steel blue 1", 0xffcae1ff);
  namer.add("light steel blue 2", 0xffbcd2ee);
  namer.add("light steel blue 3", 0xffa2b5cd);
  namer.add("light steel blue 4", 0xff6e7b8b);
  namer.add("light yellow", 0xffffffe0);
  namer.add("light yellow 1", 0xffffffe0);
  namer.add("light yellow 2", 0xffeeeed1);
  namer.add("light yellow 3", 0xffcdcdb4);
  namer.add("light yellow 4", 0xff8b8b7a);
  namer.add("lime", 0xff00ff00);
  namer.add("lime green", 0xff32cd32);
  namer.add("limegreen", 0xff32cd32);
  namer.add("linen", 0xfffaf0e6);
  namer.add("magenta 2", 0xffee00ee);
  namer.add("magenta 3", 0xffcd00cd);
  namer.add("magenta 4", 0xff8b008b);
  namer.add("manganese blue", 0xff03a89e);
  namer.add("maroon", 0xff800000);
  namer.add("maroon 1", 0xffff34b3);
  namer.add("maroon 2", 0xffee30a7);
  namer.add("maroon 3", 0xffcd2990);
  namer.add("maroon 4", 0xff8b1c62);
  namer.add("medium orchid", 0xffba55d3);
  namer.add("medium orchid 1", 0xffe066ff);
  namer.add("medium orchid 2", 0xffd15fee);
  namer.add("medium orchid 3", 0xffb452cd);
  namer.add("medium orchid 4", 0xff7a378b);
  namer.add("medium purple", 0xff9370db);
  namer.add("medium purple 1", 0xffab82ff);
  namer.add("medium purple 2", 0xff9f79ee);
  namer.add("medium purple 3", 0xff8968cd);
  namer.add("medium purple 4", 0xff5d478b);
  namer.add("medium sea green", 0xff3cb371);
  namer.add("medium seagreen", 0xff3cb371);
  namer.add("medium slate blue", 0xff7b68ee);
  namer.add("medium slateblue", 0xff7b68ee);
  namer.add("medium spring green", 0xff00fa9a);
  namer.add("medium turquoise", 0xff48d1cc);
  namer.add("medium violet red", 0xffc71585);
  namer.add("medium violetred", 0xffc71585);
  namer.add("melon", 0xffe3a869);
  namer.add("midnight blue", 0xff191970);
  namer.add("mint", 0xffbdfcc9);
  namer.add("mint cream", 0xfff5fffa);
  namer.add("misty rose", 0xffffe4e1);
  namer.add("misty rose 1", 0xffffe4e1);
  namer.add("misty rose 2", 0xffeed5d2);
  namer.add("misty rose 3", 0xffcdb7b5);
  namer.add("misty rose 4", 0xff8b7d7b);
  namer.add("moccasin", 0xffffe4b5);
  namer.add("navajo white", 0xffffdead);
  namer.add("navajo white 1", 0xffffdead);
  namer.add("navajo white 2", 0xffeecfa1);
  namer.add("navajo white 3", 0xffcdb38b);
  namer.add("navajo white 4", 0xff8b795e);
  namer.add("navy", 0xff000080);
  namer.add("none", 0xff00000000);
  namer.add("old lace", 0xfffdf5e6);
  namer.add("olive", 0xff808000);
  namer.add("olive drab", 0xff6b8e23);
  namer.add("olive drab 1", 0xffc0ff3e);
  namer.add("olive drab 2", 0xffb3ee3a);
  namer.add("olive drab 3", 0xff9acd32);
  namer.add("olive drab 4", 0xff698b22);
  namer.add("orange", 0xffffa500);
  namer.add("orange 1", 0xffffa500);
  namer.add("orange 2", 0xffee9a00);
  namer.add("orange 3", 0xffcd8500);
  namer.add("orange 4", 0xff8b5a00);
  namer.add("orange red", 0xffff4500);
  namer.add("orange red 1", 0xffff4500);
  namer.add("orange red 2", 0xffee4000);
  namer.add("orange red 3", 0xffcd3700);
  namer.add("orange red 4", 0xff8b2500);
  namer.add("orchid", 0xffda70d6);
  namer.add("orchid 1", 0xffff83fa);
  namer.add("orchid 2", 0xffee7ae9);
  namer.add("orchid 3", 0xffcd69c9);
  namer.add("orchid 4", 0xff8b4789);
  namer.add("pale goldenrod", 0xffeee8aa);
  namer.add("pale green", 0xff98fb98);
  namer.add("pale green 1", 0xff9aff9a);
  namer.add("pale green 2", 0xff90ee90);
  namer.add("pale green 3", 0xff7ccd7c);
  namer.add("pale green 4", 0xff548b54);
  namer.add("pale turquoise", 0xffafeeee);
  namer.add("pale turquoise 1", 0xffbbffff);
  namer.add("pale turquoise 2", 0xffaeeeee);
  namer.add("pale turquoise 3", 0xff96cdcd);
  namer.add("pale turquoise 4", 0xff668b8b);
  namer.add("pale violet red", 0xffdb7093);
  namer.add("pale violet red 1", 0xffff82ab);
  namer.add("pale violet red 2", 0xffee799f);
  namer.add("pale violet red 3", 0xffcd6889);
  namer.add("pale violet red 4", 0xff8b475d);
  namer.add("papaya whip", 0xffffefd5);
  namer.add("peachpuff", 0xffffdab9);
  namer.add("peachpuff 1", 0xffffdab9);
  namer.add("peachpuff 2", 0xffeecbad);
  namer.add("peachpuff 3", 0xffcdaf95);
  namer.add("peachpuff 4", 0xff8b7765);
  namer.add("peacock", 0xff33a1c9);
  namer.add("peru", 0xffcd853f);
  namer.add("pink", 0xffffc0cb);
  namer.add("pink 1", 0xffffb5c5);
  namer.add("pink 2", 0xffeea9b8);
  namer.add("pink 3", 0xffcd919e);
  namer.add("pink 4", 0xff8b636c);
  namer.add("plum", 0xffdda0dd);
  namer.add("plum 1", 0xffffbbff);
  namer.add("plum 2", 0xffeeaeee);
  namer.add("plum 3", 0xffcd96cd);
  namer.add("plum 4", 0xff8b668b);
  namer.add("powder blue", 0xffb0e0e6);
  namer.add("purple", 0xff800080);
  namer.add("purple 1", 0xff9b30ff);
  namer.add("purple 2", 0xff912cee);
  namer.add("purple 3", 0xff7d26cd);
  namer.add("purple 4", 0xff551a8b);
  namer.add("raspberry", 0xff872657);
  namer.add("raw sienna", 0xffc76114);
  namer.add("red", 0xffff0000);
  namer.add("red 1", 0xffff0000);
  namer.add("red 2", 0xffee0000);
  namer.add("red 3", 0xffcd0000);
  namer.add("red 4", 0xff8b0000);
  namer.add("rosy brown", 0xffbc8f8f);
  namer.add("rosy brown 1", 0xffffc1c1);
  namer.add("rosy brown 2", 0xffeeb4b4);
  namer.add("rosy brown 3", 0xffcd9b9b);
  namer.add("rosy brown 4", 0xff8b6969);
  namer.add("royal blue", 0xff4169e1);
  namer.add("royal blue 1", 0xff4876ff);
  namer.add("royal blue 2", 0xff436eee);
  namer.add("royal blue 3", 0xff3a5fcd);
  namer.add("royal blue 4", 0xff27408b);
  namer.add("saddle brown", 0xff8b4513);
  namer.add("salmon", 0xfffa8072);
  namer.add("salmon 1", 0xffff8c69);
  namer.add("salmon 2", 0xffee8262);
  namer.add("salmon 3", 0xffcd7054);
  namer.add("salmon 4", 0xff8b4c39);
  namer.add("sandy brown", 0xfff4a460);
  namer.add("sap green", 0xff308014);
  namer.add("sea green", 0xff2e8b57);
  namer.add("sea green 1", 0xff54ff9f);
  namer.add("sea green 2", 0xff4eee94);
  namer.add("sea green 3", 0xff43cd80);
  namer.add("sea green 4", 0xff2e8b57);
  namer.add("seashell", 0xfffff5ee);
  namer.add("seashell 1", 0xfffff5ee);
  namer.add("seashell 2", 0xffeee5de);
  namer.add("seashell 3", 0xffcdc5bf);
  namer.add("seashell 4", 0xff8b8682);
  namer.add("sepia", 0xff5e2612);
  namer.add("sienna", 0xffa0522d);
  namer.add("sienna 1", 0xffff8247);
  namer.add("sienna 2", 0xffee7942);
  namer.add("sienna 3", 0xffcd6839);
  namer.add("sienna 4", 0xff8b4726);
  namer.add("silver", 0xffc0c0c0);
  namer.add("sky blue", 0xff87ceeb);
  namer.add("sky blue 1", 0xff87ceff);
  namer.add("sky blue 2", 0xff7ec0ee);
  namer.add("sky blue 3", 0xff6ca6cd);
  namer.add("sky blue 4", 0xff4a708b);
  namer.add("slate blue", 0xff6a5acd);
  namer.add("slate blue 1", 0xff836fff);
  namer.add("slate blue 2", 0xff7a67ee);
  namer.add("slate blue 3", 0xff6959cd);
  namer.add("slate blue 4", 0xff473c8b);
  namer.add("slate grey", 0xff708090);
  namer.add("slate grey 1", 0xffc6e2ff);
  namer.add("slate grey 2", 0xffb9d3ee);
  namer.add("slate grey 3", 0xff9fb6cd);
  namer.add("slate grey 4", 0xff6c7b8b);
  namer.add("snow", 0xfffffafa);
  namer.add("snow 1", 0xfffffafa);
  namer.add("snow 2", 0xffeee9e9);
  namer.add("snow 3", 0xffcdc9c9);
  namer.add("snow 4", 0xff8b8989);
  namer.add("spring green", 0xff00ff7f);
  namer.add("spring green 1", 0xff00ee76);
  namer.add("spring green 2", 0xff00cd66);
  namer.add("spring green 3", 0xff008b45);
  namer.add("steel blue", 0xff4682b4);
  namer.add("steel blue 1", 0xff63b8ff);
  namer.add("steel blue 2", 0xff5cacee);
  namer.add("steel blue 3", 0xff4f94cd);
  namer.add("steel blue 4", 0xff36648b);
  namer.add("tan", 0xffd2b48c);
  namer.add("tan 1", 0xffffa54f);
  namer.add("tan 2", 0xffee9a49);
  namer.add("tan 3", 0xffcd853f);
  namer.add("tan 4", 0xff8b5a2b);
  namer.add("teal", 0xff008080);
  namer.add("thistle", 0xffd8bfd8);
  namer.add("thistle 1", 0xffffe1ff);
  namer.add("thistle 2", 0xffeed2ee);
  namer.add("thistle 3", 0xffcdb5cd);
  namer.add("thistle 4", 0xff8b7b8b);
  namer.add("tomato", 0xffff6347);
  namer.add("tomato 1", 0xffff6347);
  namer.add("tomato 2", 0xffee5c42);
  namer.add("tomato 3", 0xffcd4f39);
  namer.add("tomato 4", 0xff8b3626);
  namer.add("turquoise", 0xff40e0d0);
  namer.add("turquoise 1", 0xff00f5ff);
  namer.add("turquoise 2", 0xff00e5ee);
  namer.add("turquoise 3", 0xff00c5cd);
  namer.add("turquoise 4", 0xff00868b);
  namer.add("turquoise blue", 0xff00c78c);
  namer.add("violet", 0xffee82ee);
  namer.add("violet red", 0xffd02090);
  namer.add("violet red 1", 0xffff3e96);
  namer.add("violet red 2", 0xffee3a8c);
  namer.add("violet red 3", 0xffcd3278);
  namer.add("violet red 4", 0xff8b2252);
  namer.add("warm grey", 0xff808069);
  namer.add("wheat", 0xfff5deb3);
  namer.add("wheat 1", 0xffffe7ba);
  namer.add("wheat 2", 0xffeed8ae);
  namer.add("wheat 3", 0xffcdba96);
  namer.add("wheat 4", 0xff8b7e66);
  namer.add("white", 0xffffffff);
  namer.add("white smoke", 0xfff5f5f5);
  namer.add("yellow", 0xffffff00);
  namer.add("yellow 1", 0xffffff00);
  namer.add("yellow 2", 0xffeeee00);
  namer.add("yellow 3", 0xffcdcd00);
  namer.add("yellow 4", 0xff8b8b00);
#if 0
  for (auto i = 1; i < 100; ++i) {
    auto argb = 0xff000000 + 0x10101 * ((i * 0xff) / 100);
    namer.add("grey " + to_string(i), argb);
  }
#endif

  return namer;
}

static const ColorNamer NAMER = makeNamer();

static const char GREY_MARKER[] = "grey";

} // namespace

bool nameToRgb(const string& cname, FColor* color) {
  auto name = replace(cname, " ", "");
  lower(&name);
  name = replace(name, "gray", "grey");
  if (name.empty())
    return false;

  auto hasHash = (name[0] == '#');
  if (hasHash or isHex(name)) {
    *color = FColor(fromHex(&name[hasHash ? 1 : 0]));
    return true;
  }

  auto i = NAMER.stringToColor_.find(name);
  auto success = (i != NAMER.stringToColor_.end());
  if (success) {
    *color = FColor(i->second);
  } else if (not name.find(GREY_MARKER)) {
    auto start = name.c_str();
    auto p = start + strlen(GREY_MARKER);
    for (; isspace(*p); ++p);
    char* endptr;
    auto f = roundf(strtof(p, &endptr) * 100.0f) / 10000.0f;
    if (not *endptr and f >= 0.0f and f <= 1.0f) {
      *color = FColor(f, f, f);
      success = true;
    }
  }
  return success;
}

string rgbToName(const FColor& color) {
  string suffix;
  FColor c = color;
  if (c.alpha() < 1.0f) {
    suffix = ", alpha=" + toString(c.alpha()) + "]";
    c.alpha() = 1.0f;
  }

  auto i = NAMER.colorToString_.find(c);
  string name;
  if (i != NAMER.colorToString_.end()) {
    name = i->second;
    if (not suffix.empty())
      name = "[" + name;
  } else if (c.isGrey()) {
    name = "grey " + toPercent(c.red());
    if (not suffix.empty())
      name = "[" + name;
  } else {
    name = "[red=" + toString(c.red()) +
        ", green=" + toString(c.green()) +
        ", blue=" + toString(c.blue());
    if (suffix.empty())
      suffix += "]";
  }
  return name + suffix;
}

}  // namespace color
}  // namespace echomesh
