#include "echomesh/color/Tile.h"
#include "echomesh/color/Rows.h"

namespace echomesh {
namespace color {

static
FColorList tile(FColorList const& fcl,
                Point const& tileSize,
                Point const& boardSize,
                Point const& offset) {
    FColorList result;
    result.reserve(boardSize.first * boardSize.second);

    for (auto y = 0; y < boardSize.second; ++y) {
        auto tileY = ((y + offset.second) % tileSize.second) * tileSize.first;
        for (auto x = 0; x < boardSize.first; ++x) {
            auto tileX = (x + offset.first) % tileSize.first;
            result.push_back(fcl.get(tileY + tileX));
        }
    }

    return result;
}

static int getOffset(int centering, int tileSize, int boardSize) {
    if (centering < 0)
        return 0;

    int offset = abs(boardSize - tileSize);
    if (!centering)
        offset /= 2;
    return offset;
}

FColorList tile(const FColorList& fcl, int xMult, int yMult, int columns) {

    auto rows = computeRows(fcl.size(), columns);
    auto newColumns = columns * xMult;
    auto newRows = rows * yMult;

    return tile(fcl, {columns, rows}, {newColumns, newRows}, {});
}

FColorList tile_pieces(const FColorList& fcl, int tileColumns,
                       int boardColumns, int boardRows,
                       int xCenter, int yCenter) {
    auto tileRows = computeRows(fcl.size(), tileColumns);
    auto offsetColumn = getOffset(xCenter, tileColumns, boardColumns);
    auto offsetRow = getOffset(yCenter, tileRows, boardRows);
    return tile(fcl,
                {tileColumns, tileRows},
                {boardColumns, boardRows},
                {offsetColumn, offsetRow});
}

}  // namespace color
}  // namespace echomesh
