"""Rebuild models/manifest.json from whatever .obj files are sitting in models/.

A browser cannot list a folder, so gallery mode reads this file instead.
Run it after every export. The test cube is left out on purpose.

Models are ordered by the number MagicaVoxel puts in the filename
("...-2-stereo rack.obj"), so the row on screen keeps the layer order
from the scene they came out of.
"""
import json
import re
from pathlib import Path

MODELS = Path(__file__).parent / "models"


def order(name: str) -> int:
    match = re.search(r"-(\d+)-", name)
    return int(match.group(1)) if match else 999


def main() -> None:
    names = sorted(
        (p.name for p in MODELS.glob("*.obj") if p.name != "test-cube.obj"),
        key=order,
    )
    (MODELS / "manifest.json").write_text(
        json.dumps({"models": names}, indent=2), encoding="utf-8"
    )
    print(f"manifest.json written with {len(names)} model(s):")
    for n in names:
        print(f"  {n}")


if __name__ == "__main__":
    main()
