#!/usr/bin/env python3
"""Cache the small OSM tile set needed by selected daily-card prototypes."""

from __future__ import annotations

import argparse
import json
import math
import time
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "daily-cards"
TILES = DATA / "tiles"
USER_AGENT = "SP-FR-guidebook-daily-card-builder/1.0 (prototype tile cache)"
MAP_WIDTH, MAP_HEIGHT = 746, 1118


def world_pixel(lat: float, lng: float, zoom: int) -> tuple[float, float]:
    scale = 256 * 2**zoom
    sin_lat = math.sin(math.radians(lat))
    return ((lng + 180) / 360 * scale,
            (0.5 - math.log((1 + sin_lat) / (1 - sin_lat)) / (4 * math.pi)) * scale)


def required_tiles(day: dict) -> list[tuple[int, int, int]]:
    zoom = day["map"]["zoom"]
    cx, cy = world_pixel(day["map"]["center"][0], day["map"]["center"][1], zoom)
    left, right = cx - MAP_WIDTH / 2 - 256, cx + MAP_WIDTH / 2 + 256
    top, bottom = cy - MAP_HEIGHT / 2 - 256, cy + MAP_HEIGHT / 2 + 256
    limit = 2**zoom
    return [(zoom, x % limit, y) for x in range(math.floor(left/256), math.floor(right/256)+1)
            for y in range(max(0, math.floor(top/256)), min(limit-1, math.floor(bottom/256))+1)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("days", nargs="*", type=int, default=[2, 4, 5])
    args = parser.parse_args()
    wanted = set()
    for number in args.days:
        day = json.loads((DATA / f"day-{number:02d}.json").read_text(encoding="utf-8"))
        wanted.update(required_tiles(day))
    downloaded = 0
    for zoom, x, y in sorted(wanted):
        target = TILES / str(zoom) / str(x) / f"{y}.png"
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        request = urllib.request.Request(
            f"https://tile.openstreetmap.org/{zoom}/{x}/{y}.png",
            headers={"User-Agent": USER_AGENT, "Referer": "https://github.com/jeongjae/SP-FR-guidebook", "Connection": "close"},
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            target.write_bytes(response.read())
        downloaded += 1
        time.sleep(0.03)
    print(f"tiles ready: {len(wanted)} required, {downloaded} downloaded", flush=True)


if __name__ == "__main__":
    main()
