"""Entry program: copy the bundled front-page image to the output path.

Standard library only. No network, no timestamps, no randomness: the
output is byte for byte the PNG this repository holds, so repeated runs
are identical.
"""

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    src = here / "assets" / "entry.png"
    if not src.exists():
        raise SystemExit(f"missing bundled image: {src}")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
