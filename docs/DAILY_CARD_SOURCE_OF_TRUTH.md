# Daily Action Map — Source of Truth audit

Audit date: 2026-08-05  
Working branch: `jeongjae/daily-action-map`  
Baseline commit: `f95d1f4f5a1823262665316ed3b216fc6987522c`

## Decision

The repository currently contains two schedule states. They must not be silently
combined.

1. `main` declares `source/CURRENT/00_Governance/00_Current_Source_of_Truth_Index_v2.0.md`
   as the authoritative index. Its master itinerary is v1.2, updated 2026-08-01.
2. Local branch `feat/itinerary-marseille-arles` at
   `43b1ce441fbcf54496703165024c305295f396cc` contains a newer master itinerary
   (document version v1.3, updated 2026-08-04), but it has not been merged into
   `main`.

The daily-card dataset is bootstrapped from the newer branch so the prototypes
do not immediately become obsolete. Every affected record retains
`sourceStatus: "candidate-latest-needs-review"`. This is not a declaration that
the unmerged branch is approved.

## Material conflicts

| Area | `main` | Newer candidate branch | Handling |
|---|---|---|---|
| Luberon | 4 nights, through 9/17 | 3 nights, checkout 9/16 | candidate data + needs-review |
| Avignon | 9/17–9/21 | 9/16–9/20 | candidate data + needs-review |
| Lyon | 9/21–9/25 | 9/20–9/24 | candidate data + needs-review |
| Paris | 15 nights from 9/25 | 16 nights from 9/24 | candidate data + needs-review |
| Day 14 | Cassis/Calanques | Marseille by public transport | candidate data + needs-review |
| Day 19 | Luberon recovery day | Luberon checkout → Avignon | candidate data + needs-review |
| Day 22 | Uzès/Pont du Gard | Arles day trip | candidate data + needs-review |
| Day 23–28 | old regional numbering | Lyon/Paris transition shifted one day earlier | candidate data + needs-review |

The prototype days are deliberately outside the conflict range:

- Day 02 — Barcelona walking/public-transport pattern
- Day 05 — Bàscara–Collioure–Cadaqués rental-car loop
- Day 04 — Barcelona–Sitges–Bàscara inter-city transfer

## Authoritative inputs by responsibility

| Responsibility | Source |
|---|---|
| Declared content governance | `source/CURRENT/00_Governance/00_Current_Source_of_Truth_Index_v2.0.md` |
| Candidate 43-day mapping | `feat/itinerary-marseille-arles:source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md` |
| Candidate execution constraints | `feat/itinerary-marseille-arles:source/OPERATIONS/100_Whole_Trip_43_Day_Execution_Audit_v1.0.md` |
| Day-level times and actions | authoritative regional chapters under `source/CURRENT/20_Regional_Chapters/` |
| Existing verified/approximate coordinates | `source/ASSETS/76_Daily_Execution_Maps/daily-maps.json` and place registry |
| Prototype driving geometry | cached OSRM GeoJSON, fetched by `scripts/daily-cards/cache_routes.py` |
| Basemap | locally cached OpenStreetMap tiles with visible attribution |

Archived v1.x chapters, Reader editions, and legacy card PNGs are not schedule
sources. Existing card images are display artifacts and contain truncated text
and schematic rather than geographic maps.

## Needs review before the first five-card batch

1. Approve or merge the `feat/itinerary-marseille-arles` schedule state.
2. Lock Day 07 Bàscara → Nice transport and rental-car return structure.
3. Confirm every accommodation name/address. Candidate hotels are never treated
   as confirmed; private lodging coordinates remain approximate and are not
   exported as public navigation links.
4. Lock train/flight times, booking times, parking, and restaurant reservations.
5. Extend coordinate and route review beyond the three prototype days. Missing
   values remain machine-visible in each JSON file and in the QA report.

