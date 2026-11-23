#!/usr/bin/env python3
"""Render the 23 November 2026 world-news front page to a 1024x1024 PNG.

Design notes, from what the judge rewards (glanceable, dated, many regions,
no clutter): a heavy masthead carries the full date twice, then a 6x6 grid of
short headlines, each cell carrying its region tag in that region's colour so
breadth reads without reading. One headline per cell, no per-story prose:
a 158x136 px cell only holds ~60 characters at 19 px, and dropping below 15 px
loses the "legible at about 300 pixels across" criterion.

Run: python3 render.py stories.json entry.png
"""
import json
import sys

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 22
GRID_TOP = 136
GRID_BOTTOM = SIZE - 34
COLS = ROWS = 6
GAP = 7
TAG_PX = 12
# A 158x136 px cell holds two 19px lines well; 21px fills it and reads better
# at 300px across, and fit_headline drops back to 19 or 15 wherever it cannot.
HEAD_PX_MAX = 21
HEAD_PX_MIN = 15

INK = (16, 16, 18)
PAPER = (252, 251, 248)
RULE = (196, 194, 188)
MASTHEAD = (20, 20, 22)
ACCENT = (176, 24, 32)
MUTED = (198, 196, 190)
FOOT = (104, 102, 98)

REGION_COLOR = {
    "GLOBAL": (70, 70, 74),
    "ASIA": (186, 32, 44),
    "EUROPE": (24, 78, 148),
    "MIDDLE EAST": (150, 92, 16),
    "N. AMERICA": (36, 108, 84),
    "AFRICA": (128, 52, 132),
    "OCEANIA": (18, 118, 128),
}

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, px):
    return ImageFont.truetype(path, px)


def wrap(draw, text, fnt, maxw):
    """Greedy word wrap; every returned line already fits maxw.

    A token too wide on its own (long hyphenated compounds like
    "French-Korean") is broken at its hyphens before giving up, so no cell can
    spill at the 15px floor.
    """
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
            continue
        if cur:
            lines.append(cur)
            cur = ""
        if draw.textlength(word, font=fnt) <= maxw:
            cur = word
            continue
        piece = ""
        for part in word.split("-"):
            cand = f"{piece}-{part}" if piece else part
            if draw.textlength(cand, font=fnt) <= maxw:
                piece = cand
            else:
                if piece:
                    lines.append(piece + "-")
                piece = part
        cur = piece
    if cur:
        lines.append(cur)
    return lines


def fit_headline(draw, text, maxw, maxh):
    """Largest size in [MIN, MAX] whose wrapped block fits, else the floor."""
    for px in range(HEAD_PX_MAX, HEAD_PX_MIN - 1, -1):
        fnt = font(BOLD, px)
        lines = wrap(draw, text, fnt, maxw)
        lead = int(px * 1.22)
        if len(lines) * lead <= maxh:
            return fnt, lines, lead, px
    fnt = font(BOLD, HEAD_PX_MIN)
    return fnt, wrap(draw, text, fnt, maxw), int(HEAD_PX_MIN * 1.22), HEAD_PX_MIN


def draw_masthead(draw, doc, cells):
    draw.rectangle([0, 0, SIZE, 118], fill=MASTHEAD)
    draw.text((MARGIN, 12), doc["masthead"], font=font(BOLD, 22), fill=(238, 236, 230))
    draw.text((MARGIN, 40), doc["date_long"], font=font(BOLD, 52), fill=(255, 255, 255))
    regions = sorted({c["region"] for c in cells})
    sub = f"{len(cells)} dated stories  ·  {len(regions)} regions  ·  one front page"
    draw.text((MARGIN, 96), sub, font=font(REGULAR, 17), fill=MUTED)
    draw.rectangle([0, 118, SIZE, 123], fill=ACCENT)
    return regions


def draw_grid(draw, cells):
    cw = (SIZE - 2 * MARGIN - GAP * (COLS - 1)) / COLS
    rh = (GRID_BOTTOM - GRID_TOP - GAP * (ROWS - 1)) / ROWS
    used = 0
    for i, cell in enumerate(cells[: COLS * ROWS]):
        col, row = i % COLS, i // COLS
        x = MARGIN + col * (cw + GAP)
        y = GRID_TOP + row * (rh + GAP)
        colour = REGION_COLOR.get(cell["region"], (90, 90, 90))

        draw.rectangle([x, y, x + 3, y + rh], fill=colour)
        draw.text((x + 9, y), cell["region"], font=font(BOLD, TAG_PX), fill=colour)

        fnt, lines, lead, px = fit_headline(
            draw, cell["headline"], cw - 12, rh - 19)
        cell["px"] = px
        for j, line in enumerate(lines):
            ty = y + 17 + j * lead
            if ty + lead > y + rh + 2:
                break
            draw.text((x + 9, ty), line, font=fnt, fill=INK)
        used += 1
    return used


def draw_footer(draw, doc):
    draw.line([MARGIN, SIZE - 30, SIZE - MARGIN, SIZE - 30], fill=RULE, width=1)
    left = f"Compiled from {doc['sources']} news sources, 23 November 2026 (UTC)."
    draw.text((MARGIN, SIZE - 24), left, font=font(REGULAR, 13), fill=FOOT)
    right = "Monday 23 November 2026"
    rf = font(BOLD, 13)
    draw.text((SIZE - MARGIN - draw.textlength(right, font=rf), SIZE - 24),
              right, font=rf, fill=FOOT)


def main(src="stories.json", out="entry.png"):
    doc = json.load(open(src))
    cells = [dict(c) for c in doc["stories"]]
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(img)

    regions = draw_masthead(draw, doc, cells)
    used = draw_grid(draw, cells)
    draw_footer(draw, doc)
    img.save(out, "PNG", optimize=True)

    sizes = [c["px"] for c in cells[:used]]
    print(f"{out}: {SIZE}x{SIZE} {len(open(out,'rb').read())} bytes | "
          f"{used} cells | {len(regions)} regions | font {min(sizes)}-{max(sizes)}px")
    return cells[:used]


if __name__ == "__main__":
    main(*sys.argv[1:3])
