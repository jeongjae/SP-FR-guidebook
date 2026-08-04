# 37. Source of Truth and Supersession Matrix v1.1

## A. Current-versus-archive rule

| Layer | Location | Use |
|---|---|---|
| Current | `CURRENT/` | Editing and publication source |
| Assets | `ASSETS/` | Maps, mobile cards, image plans |
| Operations | `OPERATIONS/` | Booking, decision, and re-verification control |
| Publication | `PUBLICATION/` | Future Word/PDF outputs only |
| Archive | `ARCHIVE/` | Historical reference; non-authoritative |

## B. Authoritative chapter matrix

| Region | Current authoritative file | Reader counterpart | Superseded files |
|---|---|---|---|
| Barcelona | `04_Barcelona_Sitges_v1.2.md` | `04_Barcelona_Sitges_Reader_v1.1.md` | v1.1 and earlier |
| Girona | `05_Girona_Collioure_Emporda_v1.2.md` | `05_Girona_Collioure_Emporda_Reader_v1.1.md` | v1.1 and earlier; Costa Brava v0.1 |
| Nice | `06_Nice_Cote_d_Azur_v1.4.md` | `06_Nice_Cote_d_Azur_Reader_v1.1.md` | v1.3 and earlier |
| Aix | `07_Aix_en_Provence_v1.3.md` | `07_Aix_en_Provence_Reader_v1.2.md` | v1.2 and earlier |
| Luberon | `08_Luberon_Farmhouse_v1.4.md` | `08_Luberon_Farmhouse_Reader_v1.2.md` | v1.3 and earlier |
| Avignon | `09_Avignon_Alpilles_Pont_du_Gard_v1.2.md` | `09_Avignon_Alpilles_Pont_du_Gard_Reader_v1.2.md` | v1.1 and earlier |
| Lyon | `10_Lyon_v1.3.md` | `10_Lyon_Reader_v1.3.md` | v1.1 and earlier |
| Paris | `11_Paris_Long_Stay_v1.3.md` | `11_Paris_Long_Stay_Reader_v1.4.md` | v1.0 and earlier |

## C. Superseded decisions

| Topic | Superseded | Current rule |
|---|---|---|
| Nice/Aix stay | Nice 4 nights / Aix 5 nights | Nice 5 nights / Aix 4 nights |
| Marseille | Fixed Cassis–Marseille day | Cassis default; Marseille only bad-weather alternative |
| Luberon pool | Pool as lodging criterion | Pool fully excluded from evaluation |
| Julia swimming | Required/weighted lodging condition | Optional activity only |
| Main working directory | Mixed root with many versions | `CURRENT/` only |
| Publication timing | Early Word/PDF production | Word/PDF only after MD freeze and final verification |

## D. Known synchronization debt for Phase 1

- 42-day/43-day/42-night terminology is not yet normalized in every current file.
- Reader files and Master contain unresolved map/photo placeholders.
- Current Master text understates the existence of generated map and mobile-card assets.
- Lyon and Paris have not yet received Pass C.
