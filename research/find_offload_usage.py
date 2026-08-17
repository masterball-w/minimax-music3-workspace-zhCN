import glob
import os
import re

base = r"d:\program\misc\make-music\research\diffusers-dafe3733fcfdbf3c48915fe77be3aef65b5d6a2d"
for path in glob.glob(os.path.join(base, "tests", "**", "*.py"), recursive=True):
    try:
        src = open(path, encoding="utf-8").read()
    except Exception:
        continue
    if "apply_group_offloading" in src:
        print("=" * 20, os.path.relpath(path, base))
        for i, line in enumerate(src.splitlines()):
            if "group_offloading" in line or "language_model" in line or "get_component" in line:
                print(f"{i+1}: {line.strip()}")
