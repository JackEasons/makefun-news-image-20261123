#!/usr/bin/env python3
"""Deliver the pre-rendered front page to the judge's output directory.

The picture itself is drawn by draw23.py and stored in this repository as
entry.png. This entrypoint does no drawing and needs no network: it copies
that exact file to $MAKEFUN_OUTPUT_DIR/entry.png (falling back to
/output/entry.png), creating the output directory when it is missing.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied", src, "->", dst, os.path.getsize(dst), "bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
