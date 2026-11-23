[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/Admin976/world-news-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/Admin976/world-news-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# World news, 23 November 2026

One image that sums up Monday 23 November 2026: a dated front page of 36 short
headlines across 7 regions, drawn at 1024x1024.

- `stories.json` — the 36 headlines and their region tags
- `render.py` — draws the front page with PIL (`python3 render.py stories.json entry.png`)
- `verify.py` — re-measures every cell with PIL: cell count, spill, font floor, file size
- `entry.png` — the rendered image the entry submits
- `main.py` — copies `entry.png` to `/output/entry.png`

Headlines come from a sweep of 38 news feeds for that day; nothing is invented.

## Bounty

Entered in [make.fun's *Sum up 23 November's world news in one image*](https://make.fun/bounty/news-image-20261123), $100 in USDC.

Run: `python3 render.py stories.json entry.png && python3 verify.py && MAKEFUN_OUTPUT_DIR=out python3 main.py`
