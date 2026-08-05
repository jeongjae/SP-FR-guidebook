#!/usr/bin/env python3
"""Synchronize execution-map GeoJSON, HTML point payloads, captions, and KML."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import quote_plus


ROOT = Path(__file__).resolve().parents[1]
MAPS = ROOT / "source" / "ASSETS" / "75_Execution_Maps"


def point(name: str, lat: float, lon: float, category: str, status: str) -> dict:
    return {
        "type": "Feature",
        "properties": {
            "name": name,
            "sequence": 0,
            "category": category,
            "status": status,
            "google_maps": f"https://www.google.com/maps/search/?api=1&query={quote_plus(name)}",
            "phase": "확정 일정 2026-08-04",
        },
        "geometry": {"type": "Point", "coordinates": [lon, lat]},
    }


EXTRA = {
    "Aix": [
        point("Marseille Saint-Charles", 43.3026, 5.3805, "교통", "9/11 기본 당일치기 도착점"),
        point("Vieux-Port", 43.2951, 5.3740, "핵심 방문지", "9/11 기본 일정"),
        point("Le Panier", 43.3006, 5.3674, "핵심 방문지", "9/11 기본 일정"),
        point("Mucem", 43.2967, 5.3612, "핵심 방문지", "9/11 기본 일정"),
        point("Fort Saint-Jean", 43.2959, 5.3635, "핵심 방문지", "9/11 기본 일정"),
        point("Notre-Dame de la Garde", 43.2841, 5.3712, "근교·이동지", "체력·날씨에 따른 선택"),
    ],
    "Avignon": [
        point("Arles", 43.6846, 4.6326, "교통", "9/19 철도 기본 도착점"),
        point("Arènes d’Arles", 43.6776, 4.6309, "핵심 방문지", "9/19 기본 일정"),
        point("Théâtre antique", 43.6765, 4.6279, "핵심 방문지", "9/19 기본 일정"),
        point("Place du Forum", 43.6773, 4.6272, "시장·생활", "점심·카페 휴식"),
        point("Cloître Saint-Trophime", 43.6769, 4.6285, "핵심 방문지", "일정 균형에 따른 우선 선택"),
        point("Fondation Vincent van Gogh", 43.6760, 4.6262, "핵심 방문지", "Saint-Trophime과 교환하는 선택"),
        point("La Roquette", 43.6729, 4.6249, "시장·생활", "론강변과 잇는 기본 산책"),
    ],
}


CAPTIONS = {
    "Aix": "Day 12–16 · 9/11 Marseille 기본일과 Cassis 선택 대안의 기준점. 번호는 개략 흐름이다.",
    "Luberon": "Day 16–19 · 3박 일정의 기준점. L’Isle-sur-la-Sorgue는 기본 일정이 아닌 선택 대안이다.",
    "Avignon": "Day 19–23 · Avignon·Uzès·Pont du Gard·Arles 기본 일정과 Alpilles 선택 대안의 기준점.",
    "Lyon": "Day 23–27 · 9/20–9/24 Lyon과 9/23 Annecy 당일치기의 기준점.",
    "Paris": "Day 27–43 · 9/24–10/10 Paris 16박 생활권과 선택 근교의 기준점.",
}


def update_region(region: str) -> None:
    geo_path = MAPS / f"{region}_Execution_Map_v0.2.geojson"
    data = json.loads(geo_path.read_text(encoding="utf-8"))
    features = data["features"]

    if region == "Aix":
        for feature in features:
            if feature["properties"]["name"] == "Cassis":
                feature["properties"]["status"] = "선택 대안 — Marseille와 결합 금지"
        insert_at = next(i for i, f in enumerate(features) if f["properties"]["name"] == "Atelier Cézanne")
        features[insert_at:insert_at] = EXTRA[region]
    elif region == "Luberon":
        for feature in features:
            if feature["properties"]["name"] == "L’Isle-sur-la-Sorgue":
                feature["properties"]["status"] = "선택 대안 — 9/17 기본 일정 아님"
    elif region == "Avignon":
        for feature in features:
            if feature["properties"]["name"] in {"Les Baux", "Saint-Rémy"}:
                feature["properties"]["status"] = "선택 대안 — Arles 전체 교체 시만"
        insert_at = next(i for i, f in enumerate(features) if f["properties"]["name"] == "Les Baux")
        features[insert_at:insert_at] = EXTRA[region]

    for i, feature in enumerate(features, 1):
        feature["properties"]["sequence"] = i
    geo_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    html_path = MAPS / f"{region}_Execution_Map_v0.2.html"
    page = html_path.read_text(encoding="utf-8")
    points = []
    for feature in features:
        lon, lat = feature["geometry"]["coordinates"]
        p = feature["properties"]
        points.append({"name": p["name"], "lat": lat, "lon": lon, "category": p["category"], "status": p["status"], "url": p["google_maps"]})
    page = re.sub(r"const pts=.*?;\nconst colors=", f"const pts={json.dumps(points, ensure_ascii=False)};\nconst colors=", page, count=1, flags=re.S)
    page = re.sub(r"<p>Day .*?</p>", f"<p>{CAPTIONS[region]}</p>", page, count=1)
    html_path.write_text(page, encoding="utf-8")

    kml_path = MAPS / f"{region}_Execution_Map_v0.2.kml"
    placemarks = []
    for feature in features:
        lon, lat = feature["geometry"]["coordinates"]
        p = feature["properties"]
        label = html.escape(f"[{p['category']}] {p['name']}")
        description = html.escape(p["status"])
        placemarks.append(
            f"<Placemark><name>{label}</name><description>{description}</description>"
            f"<Point><coordinates>{lon},{lat},0</coordinates></Point></Placemark>"
        )
    kml_path.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<kml xmlns="http://www.opengis.net/kml/2.2"><Document>\n'
        + "\n".join(placemarks)
        + "\n</Document></kml>",
        encoding="utf-8",
    )


if __name__ == "__main__":
    for name in CAPTIONS:
        update_region(name)
