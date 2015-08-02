#pragma once

#include <memory>

#include "echomesh/base/Echomesh.h"

namespace echomesh {
namespace color {

class FColor;
class FColorList;

typedef void (*CombinerFunction)(FColor const&, FColor&);
using ColumnList = vector<int>;

enum class Combiner { XOR, ADD, SUBTRACT, MULTIPLY, DIVIDE, MIN, MAX, AND, OR };

using FColorListList = vector <FColorList*>;

FColorList combine(FColorListList const&, Combiner);
FColorList combine(FColorListList const&, CombinerFunction);

/** Not yet implemented. */
FColorList combine(FColorListList const&, ColumnList const& columns,
                   CombinerFunction);


CombinerFunction getCombinerFunction(string const&);
string combinerNames();

}  // namespace color
}  // namespace echomesh
