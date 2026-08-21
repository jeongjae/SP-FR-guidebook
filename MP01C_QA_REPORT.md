# MP-01C — Transport Content & Route Linking QA Report

**Audit Date**: 2026-08-22  
**Baseline**: MP-01A = PASS / MP-01B = PASS / EX-15 baseline maintained / 43 Days / 42 Nights / 8 Bases / 134 Canonical Places / 203 Route Segments  
**Status**: `CONTENT STATUS = FROZEN / TRIP STATUS = READY TO EXECUTE`

---

## 1. Executive Summary

| Category | Audited Count | Complete / Pass | Gaps / Mismatches | Broken Links | Verdict |
|---|---:|---:|---:|---:|:---:|
| **Transport Stops** | 42 | 42 (100%) | 0 | 0 | **PASS** |
| **Route Segments (Legs)** | 203 | 203 (100%) | 0 | 0 | **PASS** |
| **Endpoint Matching** | 203 legs | 203 / 203 (100%) | 0 | 0 | **PASS** |
| **Nice 9/7–9/8 Itinerary** | Day 10 & 11 | Complete & Decoupled | 0 | 0 | **PASS** |
| **Daily Card ↔ Map Sync** | 43 Days | 43 / 43 (100%) | 0 | 0 | **PASS** |
| **Official Guidance** | Applicable Hubs | 100% Verified | 0 | 0 | **PASS** |
| **Safety & Freeze** | SOT Preserved | 0 Leaks / 0 Loss | 0 | 0 | **PASS** |

---

## 2. Route Segment Breakdown by Transport Mode

| Mode | Count | Share (%) | Primary Role |
|---|---:|---:|---|
| **Walk** | 104 | 51.2% | Historic old town walking, park strolls, inter-venue connection |
| **Drive / Rental Car** | 34 | 16.7% | Provence farmhouse, Luberon hilltop villages, Camargue & Côte Bleue |
| **Metro / Subway** | 29 | 14.3% | Barcelona TMB & Paris RATP intra-city navigation |
| **Train / Rail (TGV/TER/Renfe)** | 16 | 7.9% | Intercity regional transfers & Côte d'Azur coastal rail |
| **Bus / Regional Coach** | 11 | 5.4% | Local village buses (e.g. Lignes d'Azur 15/82/83 to Èze/Cap-Ferrat) |
| **Taxi / Ride** | 4 | 2.0% | Luggage transfer & early morning airport transfers |
| **Tramway** | 2 | 1.0% | Nice Port Lympia & Lyon Part-Dieu tram connections |
| **Flight** | 2 | 1.0% | Long-haul international flights (ICN ↔ BCN / CDG ↔ ICN) |
| **Unconfirmed / Backup** | 1 | 0.5% | Weather-dependent optional boat transfer |
| **Total Route Segments** | **203** | **100%** | **43 Daily Cards & 43 Daily Maps 100% Connected** |

---

## 3. Key Intercity & Base Transfer Routes Verification

1. **Day 01**: ICN ➔ BCN Airport ➔ Barcelona Sants Hotel (Flight + Taxi/Aerobus, PASS)
2. **Day 04**: Barcelona ➔ Sitges (Cau Ferrat, La Zorra) ➔ Girona Hotel (Rodalies/TER + Walk, PASS)
3. **Day 07**: Girona ➔ Perpignan ➔ Collioure ➔ Nice Hotel (TER coastal cross-border, PASS)
4. **Day 12**: Nice-Ville Hertz Car Pickup ➔ Grasse ➔ Saint-Paul-de-Vence ➔ Aix-en-Provence (Drive, PASS)
5. **Day 16**: Aix-en-Provence ➔ Coustellet ➔ Bonnieux Luberon Farmhouse (Drive, PASS)
6. **Day 19**: Luberon Farmhouse ➔ Gordes ➔ Isle-sur-la-Sorgue ➔ Avignon Hotel (Drive + Check-in, PASS)
7. **Day 22**: Avignon TGV Hertz Car Return ➔ Avignon City (Drive Return, PASS)
8. **Day 23**: Avignon Centre ➔ Avignon TGV ➔ Lyon Part-Dieu ➔ Lyon Hotel (TGV InOui, PASS)
9. **Day 27**: Lyon Part-Dieu ➔ Paris Gare de Lyon ➔ 15th Arrondissement Hotel (TGV InOui, PASS)
10. **Day 43**: Paris 15th Hotel ➔ CDG Terminal 2E ➔ ICN (RER B/Taxi + Flight, PASS)

---

## 4. Nice Reschedule (9/7 Monaco/Menton vs 9/8 Villefranche/Eze) Verification

- **Day 10 (9/7)**:
  - Route: `Nice-Ville` ➔ `Le Rocher (Monaco)` ➔ `Port Hercule & Monte-Carlo` ➔ `Menton Old Town` ➔ `Le Petit Port Dinner` ➔ `Nice-Ville Return`.
  - Stale Route Audit: Zero references to Villefranche-sur-Mer or Èze on Day 10. **(PASS)**
- **Day 11 (9/8)**:
  - Route: `Nice-Ville` ➔ `Villefranche-sur-Mer (TER 7m)` ➔ `Passable / Villa Ephrussi (Bus 15 10m)` ➔ `Restaurant & Salon de Thé Béatrice (WISH-02 Lunch)` ➔ `Èze Village (Bus 15/83)` ➔ `Nice Return (Bus 82 25m)`.
  - Linkage Audit: 100% matched to Daily Card sequence and Daily Map polyline. **(PASS)**

---

## 5. Transport Official Guidance & NOT_APPLICABLE Verification

- **Official Transit Operators**: Linked to verified official sites (SNCF Connect, TER Sud, Renfe, TMB, RATP, Lignes d'Azur, TCL, Hertz France, Paris Aéroport).
- **Logical N/A Justification**:
  - Local walking legs: Official site & booking = `NOT_APPLICABLE`.
  - Driving route segments: Station ID = `NOT_APPLICABLE`.
  - No missing links or endpoints masked as N/A.

---

## 6. Validation Summary & Gate Verdict

All regression suites passed 100% with zero broken links, zero endpoint gaps, and zero content loss.

```text
MP-01C VERDICT = PASS
READY FOR MP-01D = YES
```
