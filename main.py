#!/usr/bin/env python3
"""Prime Delta — entry for make.fun news-image-20261122.

The broadsheet image (entry.png, 1024x1024, 38 stories from 22 November
2026) is rendered ahead of time by build_image.py and shipped in this
repository. The competition rules explicitly allow this shape: "the
simplest entry is a repository holding the image and a one-line program
that copies it there; a program may also draw it."

This program is that copier. It uses only the Python standard library,
needs no network and no fonts, and is deterministic: every run writes
exactly the same bytes to the output directory, as the rules require
(the program runs twice and both runs must write the same bytes).
"""

import hashlib
import os
import sys

MAX_BYTES = 1024 * 1024  # competition cap: the image is at most 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def source_path():
    """The pre-rendered image sits next to this file in the repository."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def target_path():
    """Write to $MAKEFUN_OUTPUT_DIR when set, else /output, else the cwd."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        return os.path.join(out_dir, "entry.png")
    if os.path.isdir("/output") and os.access("/output", os.W_OK):
        return os.path.join("/output", "entry.png")
    return os.path.join(os.getcwd(), "entry.png")


def main():
    src = source_path()
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        print(f"entry.png too large: {len(data)} bytes", file=sys.stderr)
        return 1
    if not data.startswith(PNG_MAGIC):
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    dst = target_path()
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        written = fh.read()
    if written != data:
        print("written file does not match the shipped image", file=sys.stderr)
        return 1
    digest = hashlib.sha256(written).hexdigest()
    print(f"entry.png OK {len(written)} bytes sha256={digest} -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
