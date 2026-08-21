# MP-01F — Home > 전체 일정 Region Navigation QA Report

**Audit Date**: 2026-08-22  
**Baseline**: MP-01A = PASS / MP-01B = PASS / MP-01C = PASS / MP-01D = PASS / MP-01E = PASS / EX-15 baseline maintained  
**Scope**: Schedule Region Navigation / 8 Canonical Bases / Dynamic Date Detection  
**Status**: `CONTENT STATUS = FROZEN / TRIP STATUS = READY TO EXECUTE`

---

## 1. Executive Summary

| Category | Audited Targets | Verified / Pass | Broken / Missing | Verdict |
|---|---:|---:|---:|:---:|
| **Region Navigation Buttons** | 8 | 8 / 8 (100%) | 0 | **PASS** |
| **Region Anchor Targets** | 8 | 8 / 8 (100%) | 0 | **PASS** |
| **Dynamic Current-Region Detection** | 10 Test Cases | 10 / 10 (100%) | 0 | **PASS** |
| **Pre-Trip State (NEXT · Barcelona)** | date < 8/29 | 100% Verified | 0 | **PASS** |
| **In-Trip State (Current Region)** | 8/29 ~ 10/10 | 100% Verified | 0 | **PASS** |
| **Post-Trip State (Trip Complete · Paris)** | date > 10/10 | 100% Verified | 0 | **PASS** |
| **Mobile Auto-Centering (390px)** | Smooth Inline Center | 100% Verified | 0 | **PASS** |
| **Keyboard Accessibility & Focus** | Tabs & Anchors | 100% Accessible | 0 | **PASS** |

---

## 2. 8 Canonical Region Navigation Crosswalk

| Region | Region ID | First Day | Target Anchor | Anchor Exists | Button Exists | Initial Range |
|---|---|:---:|---|:---:|:---:|---|
| **Barcelona** | `barcelona` | Day 1 | `#barcelona` | **YES** | **YES** | 8.29 ~ 9.1 (3박) |
| **Girona · Empordà** | `girona` | Day 4 | `#girona` | **YES** | **YES** | 9.1 ~ 9.4 (3박) |
| **Nice** | `nice` | Day 7 | `#nice` | **YES** | **YES** | 9.4 ~ 9.9 (5박) |
| **Aix** | `aix` | Day 12 | `#aix` | **YES** | **YES** | 9.9 ~ 9.13 (4박) |
| **Luberon** | `luberon` | Day 16 | `#luberon` | **YES** | **YES** | 9.13 ~ 9.16 (3박) |
| **Avignon** | `avignon` | Day 19 | `#avignon` | **YES** | **YES** | 9.16 ~ 9.20 (4박) |
| **Lyon** | `lyon` | Day 23 | `#lyon` | **YES** | **YES** | 9.20 ~ 9.24 (4박) |
| **Paris** | `paris` | Day 27 | `#paris` | **YES** | **YES** | 9.24 ~ 10.10 (16박) |

---

## 3. Dynamic Date Simulation Test Results (10/10 PASS)

1. `2026-08-22` (Pre-trip): `NEXT · Barcelona` (Active: `#barcelona`) ➔ **PASS**
2. `2026-08-29` (Day 01 Barcelona): `Barcelona` (Active: `#barcelona`) ➔ **PASS**
3. `2026-09-07` (Day 10 Nice): `Nice` (Active: `#nice`) ➔ **PASS**
4. `2026-09-10` (Day 13 Aix): `Aix` (Active: `#aix`) ➔ **PASS**
5. `2026-09-14` (Day 17 Luberon): `Luberon` (Active: `#luberon`) ➔ **PASS**
6. `2026-09-17` (Day 20 Avignon): `Avignon` (Active: `#avignon`) ➔ **PASS**
7. `2026-09-21` (Day 24 Lyon): `Lyon` (Active: `#lyon`) ➔ **PASS**
8. `2026-09-26` (Day 29 Paris): `Paris` (Active: `#paris`) ➔ **PASS**
9. `2026-10-10` (Day 43 Paris End): `Paris` (Active: `#paris`) ➔ **PASS**
10. `2026-10-11` (Post-trip): `Trip Complete · Paris` (Active: `#paris`) ➔ **PASS**

---

## 4. Gate Verdict

```text
MP-01F VERDICT = PASS
READY FOR MP-01G = YES
```
