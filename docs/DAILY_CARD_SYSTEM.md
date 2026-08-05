# Daily Action Map generation system

## Prototype gate

Only Day 02, Day 04 and Day 05 are rendered. The remaining 40 day files are
structured audit records and deliberately retain `needsReview` fields. Do not
run a five-card batch until the three prototypes are approved.

## Structure

```text
data/daily-cards/
  schema.json
  day-01.json … day-43.json
  routes/                 # cached OSRM responses
  tiles/                  # cached OSM raster tiles
templates/daily-card/
  card.html
  card.css
  card.js                  # projection + collision-free map labels
scripts/daily-cards/
  bootstrap_data.py       # one-time schedule snapshot → 43 editable JSON files
  cache_routes.py         # driving geometry cache
  cache_tiles.py          # OSM tile cache
  render.py               # HTML → PNG/WebP/thumbnail
  validate.py             # schema, artifact and visual QA
  build_all.py            # prototype-only orchestration
source/ASSETS/80_Daily_Mobile_Guide_Images/v2/
  source/                 # self-contained rendered HTML
  full/                   # 1440×1920 PNG and WebP
  thumbs/                 # 480×640 WebP
```

## Rendering

The card is code-native HTML/CSS. Geographic coordinates are projected with Web
Mercator. OSM tiles are cached locally and embedded into each source HTML. Car
routes use cached OSRM geometry; non-car prototype legs are visibly marked as
coordinate lines until a reviewed pedestrian/transit router is selected.

Map labels use measured DOM rectangles. Eight preferred offsets are tried first,
then an outward spiral. Each candidate is rejected if it touches an earlier
label, marker or map edge. The rendered DOM publishes overlap and overflow
counts for QA.

`render.py` prefers bundled Playwright Chromium. This WSL environment lacks the
system NSS libraries and cannot install them without sudo, so the local run uses
installed Windows Chrome in headless CLI mode. CI can use the Playwright path.

## Commands

```bash
python3 scripts/daily-cards/cache_routes.py 4 5
python3 scripts/daily-cards/cache_tiles.py 2 4 5
python3 scripts/daily-cards/render.py 2 4 5
python3 scripts/daily-cards/validate.py --write-report
python3 build/build.py
python3 build/hig_check.py
```

`bootstrap_data.py --force` is intentionally not part of the normal build; it
replaces edited day JSON files from a schedule ref.

## Website integration

The static-site builder discovers v2 assets before Phase 4 and legacy cards.
For v2 days it copies full PNG/WebP and thumbnail WebP into `site/assets`, shows
the thumbnail on `site/daily/day-NN.html`, and links it to the full WebP plus a
separate PNG review link. The generated `site/` directory remains untracked.

## Attribution and privacy

Every rendered map carries `© OpenStreetMap contributors`; route geometry is
identified as OSRM or coordinate-line. Private accommodation coordinates remain
approximate and must not become public Google Maps links.

