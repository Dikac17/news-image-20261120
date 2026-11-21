#!/usr/bin/env python3
"""Publish the finished front page for the 20 November 2026 news-image entry.

The artwork itself lives in ``entry.png`` next to this script; this program
only places a copy of it where the make.fun kit expects the deliverable:
inside the directory named by ``MAKEFUN_OUTPUT_DIR`` (``/output`` when the
variable is absent). Nothing is generated or altered here — the PNG is
shipped as-is and handed over unchanged.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
FALLBACK_OUTPUT = "/output"


def locate_artwork() -> Path:
    """Return the path of the artwork shipped alongside this script."""
    here = Path(__file__).resolve().parent
    artwork = here / SOURCE_NAME
    if not artwork.is_file():
        raise SystemExit(f"missing artwork: {artwork}")
    return artwork


def choose_output_folder() -> Path:
    """Pick the output folder from the environment, defaulting to /output."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return Path(raw) if raw else Path(FALLBACK_OUTPUT)


def main() -> int:
    artwork = locate_artwork()
    folder = choose_output_folder()
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / SOURCE_NAME
    shutil.copyfile(artwork, destination)
    # Guard against a truncated write: the delivered file must be exactly
    # the same size as the artwork shipped with this entry.
    if destination.stat().st_size != artwork.stat().st_size:
        raise SystemExit(f"incomplete copy: {destination}")
    print(f"copied {artwork.name} -> {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
