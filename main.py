#!/usr/bin/env python3
"""The entry program: publish the rendered front page to /output/entry.png.

The image is drawn by render.py and committed beside this file, so the run is
a copy and both runs write identical bytes. Outside the grader's container
MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))

OUT.mkdir(parents=True, exist_ok=True)
shutil.copyfile(HERE / "entry.png", OUT / "entry.png")
print(f"wrote {OUT / 'entry.png'} ({(OUT / 'entry.png').stat().st_size} bytes)")
