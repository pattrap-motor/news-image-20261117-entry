#!/usr/bin/env python3
"""Entry program: copy the shipped news image to the output directory.

The image (entry.png, 1024x1024, drawn in this repository by draw.py)
is copied byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png, so the two
grading runs write identical bytes. Standard library only, no network.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # The gate needs a whole PNG: refuse to leave a truncated copy behind.
    if os.path.getsize(dst) != os.path.getsize(src):
        raise SystemExit("entry.png copy is incomplete")


if __name__ == "__main__":
    main()
