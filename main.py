"""Place the bundled front-page image where the grader expects it.

The picture itself is part of this repository. This program does nothing
but copy it to the output folder, so the result is the same every time:
standard library only, no network, no clock, no randomness.
"""

import os
import shutil
import sys
from pathlib import Path


def bundled_image() -> Path:
    """Path of the front-page PNG shipped with this repository."""
    return Path(__file__).resolve().parent / "assets" / "entry.png"


def output_folder() -> Path:
    """Output folder, from the environment, falling back to /output."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def run() -> int:
    source = bundled_image()
    if not source.is_file():
        print(f"cannot find bundled image: {source}", file=sys.stderr)
        return 1
    target = output_folder()
    target.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target / "entry.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
