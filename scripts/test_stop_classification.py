import json
from pathlib import Path

ROOT = Path(".")
places_md = sorted((ROOT / "source" / "CURRENT" / "30_Places").glob("*.md"))
canonical_slugs = {p.stem for p in places_md}

print("Canonical places in 30_Places:", len(canonical_slugs))
