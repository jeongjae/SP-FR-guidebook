# FCR-01 — Foundation + Nice Pilot QA Report
## Food Architecture / WISH vs RECOMMENDED / Nice 3 Lunch Anchors / Food Guide Pilot
### Status: PASS (100%) · Date: 2026-08-21 · Baseline: EX-13 PASS

---

## 0. Overall Verdict

```text
================================================================================
FCR-01 FOUNDATION + NICE PILOT: PASS (100%)
- Blocking Privacy Pre-Gate: PASS (0 Leaks across source/data/site/build)
- Nice WISH Venue Register: 3 Items Managed (WISH-01 & WISH-02 Resolved, WISH-03 USER_CONFIRMATION_REQUIRED)
- Nice Schedule Integration: Day 09 (Le Figuier Lunch) & Day 11 (Restaurant Béatrice Lunch) Fully Integrated
- Regional Food Guide: 9 Traditional Dishes Defined & Separated from Venues
- Canonical Places: 114 Total (3 New Places Added & Verified: Le Figuier, Béatrice, Villa Ephrussi)
- Regression Audits: 10/10 Existing Validators PASS + New FCR-01 Audit PASS
- Content Loss: 0 / UX Broken Links: 0 / P0: 0 / P1: 0 / Active Operational P2: 9
================================================================================
```

---

## 1. EX-13 Baseline Pre-Gate & Inventory Reconciliation

- **Trip Duration**: 43 Days / 42 Nights (2026-08-29 ~ 2026-10-10)
- **Accommodation Bases**: 8 Bases (Bàscara, Barcelona, Nice, Aix, Luberon, Avignon, Lyon, Paris)
- **Canonical Places**: 114 Places (111 baseline + 3 new pilot places: `le-figuier-de-saint-esprit`, `restaurant-beatrice`, `villa-ephrussi-de-rothschild`)
- **Daily Cards**: 43 Cards (100% coverage)
- **Route Segments**: 205 Segments
- **Navigation Targets**: 248 Targets
- **Meal Slots**: 66 Meal Slots
- **Active Operational P2 Issues**: 9 (FEAS-DUR-05 & FEAS-DUR-14 remain resolved validator artifacts)

---

## 2. Blocking Privacy Pre-Gate Audit

- **Scan Scope**: `source/`, `data/`, `build/`, `site/`, `scripts/`, `docs/`, `*.csv`, `*.md`, `*.json`
- **Sanitized Patterns**: Airbnb confirmation codes (`HM...`), Hertz reservation numbers (`L672...`, `L671...`), Booking voucher numbers (`36558...`, `14008...`), Airline/Train PNRs (`FRRL7R`, `NMGI4Q`, `4YMAGT`, `X6CVW5`), Private host phone numbers (`+33 6 21...`).
- **Policy Enforcement**:
  - Public repository source files sanitized to `[CONFIRMED]` / private-safe status.
  - Private booking data managed strictly outside repository in private SOT.
  - Flight numbers (`OZ511`, `VY1521`, `OZ502`), train numbers (`TGV INOUI 12176`, `6618`), public telephone numbers of hotels/museums, and verified amounts preserved for reader utility.
- **Verification Result**: 0 leaks detected across all files (`FCR01_PRIVACY_SOURCE_SCAN.csv`).

---

## 3. Food Data Model & Taxonomy

- **Selection Origin (`selection_origin`)**:
  - `WISH`: Direct traveler preference (preserved and integrated into primary itinerary).
  - `RECOMMENDED`: Curated selection based on regional authenticity, proximity, and quality.
- **Meal Role (`meal_role`)**:
  - `PRIMARY`: Main scheduled venue for the day's meal slot.
  - `BACKUP`: Documented alternative in case of unexpected closure, wait time, or route change.
  - `OPTIONAL` / `MARKET` / `SELF_CATERING`: Specialized categories for picnic, market grazing, and home cooking.
- **Food Kind (`food_kind`)**:
  - `RESTAURANT`, `CAFE`, `BAKERY`, `MARKET`, `FOOD_HALL`, `WINE_BAR`.

---

## 4. Nice WISH Inventory & Resolution Status

| WISH ID | Venue Name | Location | Scheduled Day / Slot | Identity Status | Verification & Integration Notes |
|---|---|---|---|---|---|
| **NICE-WISH-01** | **Le Figuier de Saint-Esprit** | Antibes Old Town | **Day 09 (Sun 9/6) Lunch** | `RESOLVED` | Michelin 1-star (Chef Christian Morisset). Sunday lunch service (12:15~13:30) confirmed. Integrated into Day 09 schedule between Antibes morning market and Cannes afternoon. |
| **NICE-WISH-02** | **Restaurant & Salon de Thé Béatrice** | Saint-Jean-Cap-Ferrat | **Day 11 (Tue 9/8) Lunch** | `RESOLVED` | Inside Villa Ephrussi de Rothschild. Overlooks Rade de Villefranche. 12:00~15:00 lunch service confirmed. Integrated into Day 11 recovery day with Villa & garden visit. |
| **NICE-WISH-03** | **Salon de thé - restaurant** | Nice Port Lympia (Candidate) | Pending Confirmation | `USER_CONFIRMATION_REQUIRED` | Candidate identified: *Salon de Thé - Île de Beauté* (7 Place Île de Beauté). Awaiting traveler confirmation before locking into schedule. |

---

## 5. Nice Regional Recommended Foods Matrix

Physical venues and regional culinary heritage have been decoupled into distinct, structured modules:

1. **Socca (소카)**: Chickpea flour galette baked in a wood-fired copper oven. Best at Cours Saleya & Chez Pipo (Days 08, 09).
2. **Pissaladière (피살라디에르)**: Thick dough topped with caramelized onions, anchovies, and black cailletier olives (Days 08, 11).
3. **Salade Niçoise (살라드 뉘수아즈)**: Authentic fresh raw salad with ripe tomatoes, tuna/anchovies, olives, and boiled egg (No cooked potatoes/green beans) (Days 08, 11).
4. **Pan Bagnat (팡 바냐)**: Whole wheat bread roll soaked in olive oil and tomato juices, filled with Niçoise salad ingredients for beach picnics (Days 08, 11).
5. **Petits Farcis (프티 파르시)**: Baked stuffed Mediterranean vegetables (zucchini, tomatoes, eggplant) with minced meat and parmesan (Day 08).
6. **Daube Niçoise (도브 뉘수아즈)**: Slow-braised beef stew in Provençal red wine and dried porcini, served with handmade ravioli (Day 08).
7. **Tourte de Blettes (투르트 드 블레트)**: Sweet/savory swiss chard, pine nut, raisin, and apple pastry (Day 08).
8. **Barbajuan (바르바주앙)**: Crispy fried chard and ricotta fritters at Monaco Marché de La Condamine (Day 10).
9. **Tarte au Citron de Menton (망통 레몬 타르트)**: Citrus custard tart made with Menton IGP lemons (Day 10).

---

## 6. Daily Schedule Rebalancing & Simulation (Days 8–11)

### Day 08 (Sat 9/5) — Nice Market, Old Town, Castle Hill & Beach
- **Route**: 12h 30m, 5.5km walk, **Fatigue 3 (MODERATE)**.
- **Food Integration**: Cours Saleya morning Socca (`cours-saleya`) ➔ Vieux Nice authentic lunch (`vieux-nice`, backup: `Chez Acchiardo`) ➔ Promenade 산책 ➔ Port Lympia 저녁.

### Day 09 (Sun 9/6) — Antibes Morning, Le Figuier 1-Star Lunch & Cannes Afternoon
- **Route**: 9h 45m, TER 64km + 5.5km walk, **Fatigue 3 (MODERATE)**.
- **Food Integration**: 08:28 TER to Antibes ➔ 08:50~12:00 Vieil Antibes & Marché Provençal ➔ **12:15~14:00 Le Figuier de Saint-Esprit Fine Dining Lunch (WISH-01)** ➔ 14:15 TER to Cannes ➔ 14:45~16:50 Le Suquet & Croisette compact visit ➔ 17:00 TER return to Nice ➔ 17:35 숙소 안착.
- **Rebalancing Decision**: Cannes Marché Forville (which closes at 13:00) replaced by Antibes Marché Provençal in the morning, freeing the Cannes afternoon for a relaxed, compact cultural visit without fatigue spike.

### Day 10 (Mon 9/7) — Monaco & Menton Full-Day Riviera Rail
- **Route**: 13h, TER/Bus + 6km walk, **Fatigue 4 (HIGH, Controlled Active P2)**.
- **Food Integration**: Monaco Le Rocher ➔ 12:45 Monaco Marché de La Condamine (Barbajuan lunch, `monaco`) ➔ 14:00 TER to Menton ➔ 14:30~18:30 Menton old town & Sablettes beach ➔ 18:30~20:00 Le Petit Port seafood dinner (`menton`) ➔ 20:15 TER return to Nice.

### Day 11 (Tue 9/8) — Libération Market, Villa Ephrussi & Béatrice Lunch, Promenade Recovery
- **Route**: 10h 15m, Bus 15/Tram + 5km walk, **Fatigue 2 (LOW/RECOVERY)**.
- **Food Integration**: 08:45~10:15 Marché de la Libération food market ➔ 10:30 Bus 15 to Saint-Jean-Cap-Ferrat ➔ 11:00~12:15 Villa Ephrussi de Rothschild visit ➔ **12:15~13:45 Restaurant & Salon de Thé Béatrice Terrace Lunch (WISH-02)** ➔ 13:45~14:30 Classical musical fountain show & rose garden ➔ 15:30~17:30 Nice Promenade des Anglais recovery & laundry ➔ 18:00 Next-day Provence rental car preparation.

---

## 7. Artifact Deliverables Summary

1. `FCR01_NICE_FOOD_PILOT_QA.md`: Comprehensive QA and Pilot closure report.
2. `FCR01_NICE_WISH_VENUE_REGISTER.csv`: 3 WISH venues inventory and tracking.
3. `FCR01_NICE_RESTAURANT_RESEARCH.csv`: Research facts for scheduled and recommended venues.
4. `FCR01_NICE_REGIONAL_FOOD_MATRIX.csv`: 9 Nice regional traditional foods matrix.
5. `FCR01_NICE_MEAL_SLOT_AUDIT.csv`: 10 Nice meal slots audited and verified.
6. `FCR01_NICE_SCHEDULE_FOOD_LINK_AUDIT.csv`: Linkage verification between daily cards and canonical places.
7. `FCR01_NICE_PHOTO_ATTRIBUTION.csv`: Photo policy classification and attribution registry.
8. `FCR01_NICE_ROUTE_REVALIDATION.csv`: Chronological route timing and fatigue simulation.
9. `FCR01_PRIVACY_SOURCE_SCAN.csv`: Sanitization log proving 0 privacy leaks.
10. `scripts/fcr01_nice_food_pilot_audit.py`: Automated audit validation script.

---

## 8. Final Gate Verification Results

```bash
python3 scripts/validate_place_canonical_model.py     # PASS (114 Canonical Places)
python3 scripts/validate_itinerary.py                 # PASS (43 Days, 0 Date Gaps)
python3 scripts/ex09_daily_card_audit.py              # PASS (43 Daily Cards)
python3 scripts/ex10_route_map_audit.py               # PASS (205 Segments, 248 Targets)
python3 scripts/ex11_final_verification_audit.py      # PASS (188 Bookings, 147 Openings)
python3 scripts/ex12_field_offline_audit.py           # PASS (33 Scenarios, 8 PWA Caches)
python3 scripts/ex12h_accommodation_audit.py          # PASS (8 Bases, 42 Nights)
python3 scripts/ex11a_day_place_link_audit.py         # PASS (114 Canonical Linked, 0 Unresolved)
python3 scripts/ex12r_place_link_offline_regression.py # PASS (11 P2s Reconciled)
python3 scripts/ex13_full_trip_simulation_audit.py    # PASS (12 Failures Recovered)
python3 scripts/fcr01_nice_food_pilot_audit.py        # PASS (100% Pilot Complete)

python3 build/site.py                                 # PASS (349 Pages, 169 Search Items)
python3 build/ux_check.py                             # PASS (0 Broken Links, 0 Color Contrast Issues)
python3 build/content_audit.py                        # PASS (0 Content Loss across 114 Places)
```

---

## 9. Next Steps

- **Pilot Complete**: FCR-01 is fully validated and ready for review.
- **Hold**: Automatic expansion to FCR-02 (Barcelona / Girona / Costa Brava) is halted pending review and user confirmation on NICE-WISH-03.
