#include <map>

#include "echomesh/color/Combine.h"
#include "echomesh/color/FColorList.h"

namespace echomesh {
namespace color {

namespace {

auto COMBINERS = {
    &FColor::add,
    &FColor::subtract,
    &FColor::multiply,
    &FColor::divide,
    &FColor::min,
    &FColor::max,
    &FColor::andC,
    &FColor::orC,
    &FColor::xorC
};

void add(FColor const& from, FColor& to) {
    to.add(from);
}

void subtract(FColor const& from, FColor& to) {
    to.subtract(from);
}

void multiply(FColor const& from, FColor& to) {
    to.multiply(from);
}

void divide(FColor const& from, FColor& to) {
    to.divide(from);
}

void min(FColor const& from, FColor& to) {
    to.min(from);
}

void max(FColor const& from, FColor& to) {
    to.max(from);
}

void andC(FColor const& from, FColor& to) {
    to.andC(from);
}

void orC(FColor const& from, FColor& to) {
    to.orC(from);
}

void xorC(FColor const& from, FColor& to) {
    to.xorC(from);
}

}

FColorList combine(FColorListList const& colorLists, Combiner combiner) {
    FColorList result;
    auto size = colorLists.size();
    auto combine = COMBINERS.begin()[static_cast<int>(combiner)];

    if (size == 1) {
        result = *colorLists[0];
    } else if (size > 1) {
        size_t length = 0;
        for (auto& list: colorLists)
            length = std::max(length, list->size());
        result.reserve(length);
        for (auto i = 0; i < length; ++i) {
            auto color = (*colorLists[0])[i];
            for (auto j = 1; j < size; ++j)
                (color.*combine)(colorLists[j]->at(i));
            result.emplace_back(std::move(color));
        }
    }

    return result;
}

FColorList combine(FColorListList const& colorLists, CombinerFunction combiner) {
    FColorList result;
    auto size = colorLists.size();

    if (size == 1) {
        result = *colorLists[0];
    } else if (size > 1) {
        size_t length = 0;
        for (auto& list: colorLists)
            length = std::max(length, list->size());
        result.reserve(length);
        for (auto i = 0; i < length; ++i) {
            auto color = (*colorLists[0])[i];
            for (auto j = 1; j < size; ++j)
                combiner(colorLists[j]->at(i), color);
            result.emplace_back(std::move(color));
        }
    }

    return result;
}

static std::map <std::string, CombinerFunction> const COMBINER_MAP = {
    {"add", &add},
    {"subtract", &subtract},
    {"multiply", &multiply},
    {"divide", &divide},
    {"min", &min},
    {"max", &max},
    {"andC", &andC},
    {"orC", &orC},
    {"xorC", &xorC},
};

CombinerFunction getCombinerFunction(string const& name) {
    auto i = COMBINER_MAP.find(name);
    return i == COMBINER_MAP.end() ? nullptr : i->second;
}

string combinerNames() {
    string result;
    for (auto& i: COMBINER_MAP) {
        if (!result.empty())
            result += ", ";
        result += i.first;
    }
    return result;
}

}  // namespace color
}  // namespace echomesh
