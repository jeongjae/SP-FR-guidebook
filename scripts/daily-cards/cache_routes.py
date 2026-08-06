#!/usr/bin/env python3
"""Fetch and cache the two prototype driving routes from the public OSRM API."""

from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "daily-cards" / "routes"
USER_AGENT = "SP-FR-guidebook-daily-card-builder/1.0 (prototype route cache)"
ROUTES = {
    1: [(2.0790474, 41.2969440), (2.1476619, 41.3752738)],
    4: [(2.14005, 41.37914), (1.8086, 41.2403), (2.9101005, 42.1603007)],
    5: [(2.9101005, 42.1603007), (3.08322, 42.52505),
        (3.2584, 42.2886), (2.9101005, 42.1603007)],
    6: [(2.9101005, 42.1603007), (2.9319, 41.7195), (3.0676, 41.78),
        (3.14843, 41.97039), (3.09007, 41.97618), (2.9101005, 42.1603007)],
    12: [(7.20461, 43.65971), (7.1216304, 43.697972), (6.9228664, 43.6579121),
         (5.440842, 43.528998)],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("days", nargs="*", type=int, default=[4, 5])
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for day in args.days:
        if day not in ROUTES:
            raise SystemExit(f"no prototype route definition for Day {day:02d}")
        target = OUT / f"day-{day:02d}-driving-osrm.json"
        if target.exists() and not args.refresh:
            print(f"cached: {target.relative_to(ROOT)}")
            continue
        coordinates = ";".join(f"{lng},{lat}" for lng, lat in ROUTES[day])
        query = urllib.parse.urlencode({"overview": "full", "geometries": "geojson", "steps": "false"})
        request = urllib.request.Request(
            f"https://router.project-osrm.org/route/v1/driving/{coordinates}?{query}",
            headers={"User-Agent": USER_AGENT, "Connection": "close"},
        )
        with urllib.request.urlopen(request, timeout=45) as response:
            payload = json.loads(response.read().decode("utf-8"))
        if payload.get("code") != "Ok":
            raise SystemExit(f"OSRM failed for Day {day:02d}: {payload.get('code')}")
        target.write_text(json.dumps(payload, separators=(",", ":")) + "\n", encoding="utf-8")
        route = payload["routes"][0]
        print(f"Day {day:02d}: {route['distance']/1000:.1f}km, {route['duration']/60:.0f}min")


if __name__ == "__main__":
    main()
