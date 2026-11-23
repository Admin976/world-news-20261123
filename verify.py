#!/usr/bin/env python3
"""Self-check the rendered front page without trusting the eye.

Re-derives every cell rectangle and re-measures every drawn line with PIL, so
a headline that overflows its cell, a gap in the grid or a font below the
legibility floor fails loudly instead of shipping.
"""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

import render


def check(png="entry.png", src="stories.json"):
    doc = json.load(open(src))
    cells = doc["stories"][: render.COLS * render.ROWS]
    img = Image.open(png)
    assert img.size == (render.SIZE, render.SIZE), img.size
    assert os.path.getsize(png) <= 1048576, "over 1 MiB"

    draw = ImageDraw.Draw(img)
    cw = (render.SIZE - 2 * render.MARGIN - render.GAP * (render.COLS - 1)) / render.COLS
    rh = (render.GRID_BOTTOM - render.GRID_TOP - render.GAP * (render.ROWS - 1)) / render.ROWS
    assert len(cells) == 36, f"{len(cells)} cells, want 36"

    for i, cell in enumerate(cells):
        x = render.MARGIN + (i % render.COLS) * (cw + render.GAP)
        y = render.GRID_TOP + (i // render.COLS) * (rh + render.GAP)
        fnt, lines, lead, px = render.fit_headline(
            draw, cell["headline"], cw - 12, rh - 19)
        assert px >= render.HEAD_PX_MIN, f"cell {i} font {px}px"
        for j, line in enumerate(lines):
            bottom = y + 17 + j * lead + lead
            assert bottom <= y + rh + 2, f"cell {i} line {j} spills"
            assert draw.textlength(line, font=fnt) <= cw - 12, f"cell {i} line {j} wide"

    regions = len({c["region"] for c in cells})
    assert regions == 7, f"{regions} regions"
    print(f"OK {png}: 36 cells, {regions} regions, font >= {render.HEAD_PX_MIN}px, "
          f"{os.path.getsize(png)} bytes")


if __name__ == "__main__":
    check(*(sys.argv[1:3] or ["entry.png", "stories.json"]))
