---
title: "RS01 Phase 0 — 변경 전 기준선 스냅샷"
version: "1.0"
created: "2026-08-28"
purpose: "Verdon 1박 삽입 작업의 롤백 기준선. 이 해시가 작업 시작 시점의 정본이다."
---

# RS01 변경 전 기준선 스냅샷

## 1. 변경 전 숙박 (itinerary.json)

| key | base | checkin | checkout | nights |
|---|---|---|---|---:|
| barcelona | Barcelona | 2026-08-29 | 2026-09-01 | 3 |
| girona | Bàscara | 2026-09-01 | 2026-09-04 | 3 |
| nice | Nice | 2026-09-04 | 2026-09-09 | 5 |
| aix | Aix-en-Provence | 2026-09-09 | 2026-09-13 | 4 |
| luberon | Gordes | 2026-09-13 | 2026-09-15 | 2 |
| avignon | Avignon | 2026-09-15 | 2026-09-20 | 5 |
| lyon | Lyon | 2026-09-20 | 2026-09-24 | 4 |
| paris | Paris | 2026-09-24 | 2026-10-09 | 15 |

합계 42박 · 43일 · 지역 8개.

## 2. 변경 대상 파일 해시 (SHA256 앞 16자리)

| 파일 | 바이트 | 해시 |
|---|---:|---|
| `source/CURRENT/10_Core/itinerary.json` | 1,021 | `270a777b1bbc1bfc` |
| `source/CURRENT/10_Core/regions.json` | 6,021 | `7e2518ec2b228605` |
| `data/region-consolidation.json` | 4,266 | `36e74b7114eae778` |
| `data/region-essentials.json` | 15,360 | `9a7c47fe4d640995` |
| `data/transit-facts.json` | 35,701 | `dd2a68512f3a5ecf` |
| `data/transit-resources.json` | 5,596 | `06accb7a775a9330` |
| `data/place-days.json` | 19,004 | `1d927e087599c05d` |
| `data/map-queries.json` | 68,419 | `03651a12260951a7` |
| `source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md` | 12,394 | `62f6723edc18bb1c` |
| `source/ASSETS/91_Place_Registry_v1.0.md` | 25,239 | `a8a89cad8d94eeab` |
| `build/promote_regions.py` | 11,724 | `853a51b875d97ee4` |
| `build/content_guard.py` | 13,094 | `66cb11ba94759378` |
| `build/content_schema.json` | 7,591 | `1563f70d158e5659` |
| `data/daily-cards/day-12.json` | 8,806 | `2f55d04cc4b92c71` |
| `data/daily-cards/day-13.json` | 8,291 | `f83b8f6d4b10e1ef` |
| `data/daily-cards/day-14.json` | 11,091 | `da40739c2ae94dce` |
| `data/daily-cards/day-15.json` | 10,645 | `48cb624a7b92fdf6` |
| `data/daily-cards/day-16.json` | 9,945 | `2b1d91227eba3a3f` |
| `data/daily-cards/day-17.json` | 8,736 | `2eea32f080f22927` |
| `data/daily-cards/day-18.json` | 7,468 | `0010174533c45d27` |
| `data/daily-cards/day-19.json` | 7,565 | `43a5fcc9c05b6187` |
| `data/daily-cards/day-20.json` | 11,177 | `fae8557d1e9f3ccd` |
| `data/daily-cards/day-21.json` | 8,988 | `b49d8a53ef048867` |
| `data/daily-cards/day-22.json` | 7,881 | `337e80f510d3a1ce` |
| `source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md` | 37,513 | `d6b579afb44b3236` |
| `source/CURRENT/20_Regional_Chapters/07_Aix_en_Provence_v2.0.md` | 27,162 | `aa43606bb96b829a` |
| `source/CURRENT/20_Regional_Chapters/08_Luberon_Farmhouse_v2.0.md` | 17,156 | `38693c6259c1dc52` |
| `source/CURRENT/20_Regional_Chapters/09_Avignon_Alpilles_Pont_du_Gard_v2.0.md` | 26,059 | `3d7013cbb6ab5fbc` |

## 3. 롤백 방법

`feat/verdon-reschedule` 브랜치의 Phase 1 커밋을 되돌리면 정본 골격이
변경 전으로 복귀하고, 이후 Phase 커밋은 빌드 실패로 드러난다. 위 해시로
개별 파일의 원복 여부를 확인한다.
