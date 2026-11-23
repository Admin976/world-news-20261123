# World news, 23 November 2026

One image that sums up Monday 23 November 2026: a dated front page of 36 short
headlines across 7 regions, drawn at 1024x1024.

- `stories.json` — the 36 headlines and their region tags
- `render.py` — draws the front page with PIL (`python3 render.py stories.json entry.png`)
- `verify.py` — re-measures every cell with PIL: cell count, spill, font floor, file size
- `entry.png` — the rendered image the entry submits
- `main.py` — copies `entry.png` to `/output/entry.png`

Headlines come from a sweep of 38 news feeds for that day; nothing is invented.
