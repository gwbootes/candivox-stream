"""Rebuild models/manifest.json from whatever .obj files are sitting in models/.

A browser cannot list a folder, so gallery mode reads this file instead.
Run it after every export. The test cube is left out on purpose.

Models are ordered by the number MagicaVoxel puts in the filename
("...-2-stereo rack.obj"), so the row on screen keeps the layer order
from the scene they came out of.

Not everything exported belongs on the stage. Sizing blanks and flat logo
plates are real parts of the scene that nobody should see standing on the desk.
List those in models/exclude.txt, one piece of a filename per line, and they
stay out of every rebuild. Nothing is deleted; it simply is not listed.
"""
import json
import re
from pathlib import Path

MODELS = Path(__file__).parent / "models"
EXCLUDE_FILE = MODELS / "exclude.txt"


def order(name: str) -> int:
    match = re.search(r"-(\d+)-", name)
    return int(match.group(1)) if match else 999


def patterns() -> list:
    """Filename fragments to keep out, lowercased. Blank lines and # ignored."""
    if not EXCLUDE_FILE.exists():
        return []
    out = []
    for line in EXCLUDE_FILE.read_text(encoding="utf-8").splitlines():
        line = line.split("#")[0].strip().lower()
        if line:
            out.append(line)
    return out


def main() -> None:
    skip = patterns()
    dropped = []

    def wanted(name: str) -> bool:
        if name == "test-cube.obj":
            return False
        low = name.lower()
        for pat in skip:
            if pat in low:
                dropped.append((name, pat))
                return False
        return True

    names = sorted(
        (p.name for p in MODELS.glob("*.obj") if wanted(p.name)),
        key=order,
    )
    (MODELS / "manifest.json").write_text(
        json.dumps({"models": names}, indent=2), encoding="utf-8"
    )
    print(f"manifest.json written with {len(names)} model(s):")
    for n in names:
        print(f"  {n}")

    if dropped:
        print(f"\nleft out by exclude.txt ({len(dropped)}), files untouched:")
        for name, pat in dropped:
            print(f"  {name}   (matched '{pat}')")


if __name__ == "__main__":
    main()
