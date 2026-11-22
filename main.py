#!/usr/bin/env python3
"""Deliver the pre-rendered front page for news-image-20261122.

Entry for the make.fun bounty "Sum up 22 November's world news in one
image": the image (news-22-nov-2026.png, 1024x1024, under 1 MiB) is a
newspaper front page drawn at build time from the day's verified
headlines by tools/render_news.py; this program only copies it to
entry.png in the output directory, the way the kit's starter does.

The seven stories on the page are: the COP31 climate summit collapsing
in Antalya with no pact; a Russian drone partly collapsing a
five-storey flat near Kyiv with 14 missing; Iran striking a US radar
site in Bahrain and three tankers near Hormuz; BepiColombo reaching
Mercury orbit; the search for 36 missing after a factory fire in
Cikande, Indonesia; South Korea's education minister resigning over
the AI cheating row; and Shuri Castle reopening in Okinawa seven
years after the fire.

Pure Python standard library, deterministic, no network: both runs
write the same bytes. Honours MAKEFUN_OUTPUT_DIR, defaulting to
/output; a blank value counts as unset. The source image is checked
to be a whole PNG of the expected size before it is copied, and the
copy is verified byte for byte after writing.
"""

import hashlib
import os
import shutil
import sys

SOURCE = "news-22-nov-2026.png"
EXPECTED_SHA256 = "48a03f3dc2f822c244b67c4ce41179c5acc918597fe72843dabab2154d55a4d7"
EXPECTED_SIZE = 24830


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SOURCE)
    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) != EXPECTED_SIZE:
        print("source size mismatch: %d != %d" % (len(data), EXPECTED_SIZE),
              file=sys.stderr)
        return 1
    if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256:
        print("source sha256 mismatch", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("source is not a PNG", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    with open(dst, "rb") as fh:
        written = fh.read()
    if written != data:
        print("written copy differs from source", file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dst, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
