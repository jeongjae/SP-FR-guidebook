# Nice 공공교통 확장 — 독립 검증 결과

검증일 2026-08-21 · 대상 `codex/stay-transport-guards` @ `15a34e63`
기저 대조 `527c1c4c`(분기점) · 코드 수정 없음 · 오류 재현은 일회용 worktree 에서 수행 후 제거

---

## 최종 판정

# FAIL

**공식 요금 사실 8개는 전부 일치했고**(Solo €1.70·74분, Multi 1~100회 공동 사용, 인원수만큼 검증, 왕복·노선연장 금지, La Carte 보증금 €2, Aéro €10 무기한, 충전 카드 공항 접근, Tram 2 T1·T2↔Jean Médecin·Port Lympia), 화면·회귀도 깨끗하다. 차단 사유는 **현장 실행을 무너뜨리는 사실 오류 1건**과 **공개 배포 권리 기록 부재 1건**이다. 둘 다 국소 수정으로 해소된다.

| 항목 | 결과 |
|---|---|
| 공식 사실 8개 | **8/8 일치** |
| 추가 확인 2건(602 노선 · Day 11 환승) | **1건 정정 필요 · 1건 근거 없음** |
| 일정 대조 6줄 | 4 일치 · 1 부분일치 · 1 불일치 |
| "두 사람 약 6회" 산술 | **가정 3개 중 2개가 데이터에 근거 없음** |
| 화면·회귀 | 신규 회귀 0건 · 뷰포트 통과 · 콘솔 오류 0 |

---

## 1. 차단 이슈

### B1 — 「Villefranche → Èze Village」 버스는 항구에서 탈 수 없다

사이트가 Day 10 을 이렇게 싣는다.

```
guide/nice.html  교통 목록: "Zou! / Lignes d'Azur 버스 (Villefranche ➔ Èze Village, Èze Village ➔ Monaco)"
transit-facts    예외:      "Day 10은 TER와 광역 ZOU 602 등을 섞는다"
```

그런데 ZOU! 602 공식 시각표(`zou06_ligne602_nice_eze_monaco_juin-2026`, 2026-06-07 유효)의 정차지는
**`VILLEFRANCHE/MER Col de Villefranche`** — **Moyenne Corniche 고갯마루**이지 Villefranche-sur-Mer 항구·구시가가 아니다.
Day 10 은 TER 로 Villefranche-sur-Mer(해안 역)에 내린 뒤 버스로 Èze 로 올라가는 동선인데, **표기대로 항구에서 기다리면 버스는 오지 않는다.**

게다가 **배차가 방향당 하루 6편**이다(Nice발 08:05/10:25/12:40/15:15/17:30/19:50 · Monaco발 06:45/09:20/11:35/14:10/16:30/18:45, 앞 두 편은 일·공휴일 미운행). 이 희소한 배차가 사이트 어디에도 없다.

또 해당 leg 은 데이터에 **노선 번호가 없다**.

```
data/daily-cards/day-10.json   villefranche-sur-mer → eze-village   mode=bus  line=null  "버스/환승 약 20~25분"
data/daily-cards/day-10.json   eze-village → monaco-port-lunch      mode=bus  line=null  "버스 602 약 20분"
```

즉 어느 노선을 어디서 타는지 확정되지 않은 채 "Villefranche ➔ Èze Village" 로만 적혀 있다. 규칙 3·4 에 걸린다 — 미확정을 확정처럼 싣고 있다.

**수정**: 정류장을 `Villefranche/Mer Col de Villefranche(모옌 코르니슈)` 로 명시하고, 방향당 6편이라는 배차를 함께 싣는다. 항구에서 고갯마루까지 어떻게 올라가는지가 미확정이면 그 사실을 표시한다.

### B2 — 교통 PDF 7건이 권리 기록 없이 공개 배포된다

`c3c12eff` 가 교통국 공식 노선도 PDF 7건(**9.5 MB**)을 저장소에 넣고 사이트로 배포한다. Nice 는 `assets/transport-guides/nice/lignes-azur-main-lines-2026-09.pdf` 로 실리고 **오프라인 캐시에도 포함**된다(PWA 53.2 → 62.4 MiB).

그런데 권리 기록이 **어디에도 없다.**

```
data/transit-resources.schema.json  required: title · kind · edition · usage · officialUrl · verifiedAt · recheckBy
                                    허용 필드에도 license / rightsHolder / redistribution 없음
scripts/validate_media.py           transport-guides 미검사
87_Visual_Rights_and_Licensing_Register_v1.0.md   해당 기재 0건
```

이는 이 프로젝트가 **사진에 적용하는 기준과 정면으로 어긋난다**. CLAUDE.md 는 "gh-pages 로 공개 배포되므로 '개인 사용만 허용' 라이선스는 실제로는 쓸 수 없다 — 그건 재배포 금지다", "카탈로그에 라이선스·출처·저작자가 없는 이미지는 빌드가 거부한다" 고 못박는다. 교통국 노선도는 통상 해당 기관의 저작물이고 재배포 허용이 자명하지 않다(602 PDF 는 `© Transdev06` 표기).

**수정**: 스키마에 라이선스·권리자 필드를 필수로 넣고 7건을 채우거나, 재배포 근거가 확인될 때까지 **로컬 동봉을 빼고 공식 링크만 남긴다.** 후자는 `officialUrl` 이 이미 있어 즉시 가능하다.

> 별도 요청서 `CLAUDE_CODE_CITY_TRANSPORT_RESOURCES_VERIFICATION_REQUEST.md` 가 이 주제를 따로 다루는 것으로 보인다. 다만 이 자료가 Nice 교통 절 안에 렌더되므로 이번 판정에 포함한다.

---

## 2. 공식 사실 표

공식 페이지와 **「Guide des tarifs — ÉDITION AOÛT 2026」**(다운로드 파일명 `..._Septembre_2026`, 여행 시점 유효본) 원문을 새로 열어 확인했다.

| # | 주장 | 공식 근거 | 판정 | 보강 제안 |
|---|---|---|---|---|
| 1 | Solo €1.70 · 환승 74분 | `/fr/tickets-au-voyage` "Solo — 1 voyage … avec correspondances durant 74 minutes — 1,70 €" · 가이드 p6 | **일치** | "Solo 는 **왕복 금지**" 를 함께 표기 |
| 2 | Multi 1~100회 · 여러 사람 동시 사용 | 가이드 p6 "Chargez de 1 à 100 voyages … **Peut être utilisé simultanément par plusieurs voyageurs**" | **일치** | 체감 요금 구조 추가 가치 큼 — p7: 1~12회 €1.70 · 13~25회 €1.50 · 26~50회 €1.30 · 51회~ €1 |
| 3 | 첫 탑승·환승마다 인원수만큼 검증 | `/fr/mode-demploi` "1 validation par voyageur dans le premier véhicule / 1 validation par voyageur en cas de correspondance" | **일치** | 벌금(미검증 €40 · 무표 €60)을 적으면 현장 억지력 |
| 4 | 버스 왕복·노선연장 불가 / tram 왕복 불가 | `/fr/mode-demploi` "En bus : … ni un prolongement de parcours sur la même ligne. En tram : … mais vous pouvez effectuer des étapes dans un délai de 74 minutes" | **일치**(불완전) | **트램은 74분 안 중간 하차가 명시적으로 허용**된다. "노선 연장 불가" 는 **버스에만** 있는 조항이니 트램에 확대 적용하지 말 것 |
| 5 | La Carte 보증금 €2 · 환급 | 가이드 p2 "Coût de la carte : 2 € **remboursable**" · 기명 Ma Carte 는 "2 € non remboursable" | **일치** | 환급처를 넣을 것 — `/fr/aeroport` 가 **Arénas Presse, 455 Promenade des Anglais** 를 공항 인근 환급 판매점으로 안내. 분실 시 충전분 환급 불가도 함께 |
| 6 | Aéro 왕복 €10 · 유효기간 무제한 | `/fr/aeroport` "10€ l'aller-retour … **utilisable sans limite de validité**" | **일치** | "무제한" 은 웹 페이지에만 있고 요금 PDF 에는 없다 — 근거 URL 을 `/fr/aeroport` 로 고정 |
| 7 | 충전 카드로 공항 접근 가능 | `/fr/aeroport` "L'accès … nécessite un titre spécifique. … **Votre carte Lignes d'Azur chargée … permet également l'accès à l'aéroport**" | **일치** | 공식 문장이 앞뒤로 상충하게 읽히므로 **두 문장을 함께** 실을 것 |
| 8 | Tram 2 가 T1·T2 ↔ Jean Médecin · Port Lympia | `/fr/aeroport` 원문 그대로 | **일치** | 같은 문단의 누락 — **Tram B 도 T1·T2 를 운행**(약 10분 간격). "공항행은 2호선뿐" 으로 읽히지 않게 할 것 |
| 9 | ZOU! 602 가 Villefranche↔Èze 운행 | 602 공식 시각표 PDF | **부분 일치 — B1** | 정차지는 **Col de Villefranche** · 방향당 하루 6편 |
| 10 | Tram 1→15번 74분 1여정 가능 | 규정은 `/fr/mode-demploi` 로 성립. 15번은 Lignes d'Azur 도시요금(`ligne_15.pdf`, Lycée Masséna ↔ Port de Saint-Jean) | **규정 성립 · 소요시간 확인불가** | **공식 문서에 구간 소요시간이 없다.** 제3자 수치를 숫자로 쓰지 말 것. "74분에 빠듯할 수 있음 — 여유 없으면 1회를 더 쓴다" 로 쓰고 `{{badge:pending\|재확인}}` 처리 |

### 그 밖에 확인된 것

- **Pass 7 jours €20** 이 비교 대상에서 빠져 있다. Multi 로 1인 12회를 채우면 €20.40 이라 **손익분기가 사실상 12회**다. 5박 일정에서 검토할 가치가 있다.
- **Ticket Azur €2.50** 은 "시내 1회 + **2h30** 이내 광역 1회 환승" 이다. **74분이 아니다** — Èze·Monaco 처럼 메트로폴 밖으로 나가는 날의 표이므로 74분 규칙과 섞으면 안 된다.
- `https://www.lignesdazur.com/fr/la-carte` 는 **404**. La Carte 근거는 요금 PDF p2·p3 과 `/fr/aeroport` 로 잡을 것.
- 2026-09-01 부터 65세 이상 무료는 **메트로폴 거주자 한정**이라 여행자와 무관하다.

---

## 3. 일정 · 승차 횟수 검증

| 주장 | 판정 | 근거 |
|---|---|---|
| Day 7 "NCE T2→도심 Tram 2, 각 1회" | **일치** | `day-07.json` mode=tram, line="트램 2호선 (Ligne 2)", 약 30~40분/7km |
| Day 8 "도보" | **일치** | legs 6개 전부 walk · transport=["니스 시내 도보"] |
| Day 9 "Antibes·Cannes 별도 TER" | **일치** | train leg 3개, tram/bus leg 0. 숙소↔Nice-Ville 은 도보(0.56km) |
| Day 10 "TER와 **광역** bus 를 구간별 구매" | **불일치** | 카드 자신이 `day-10.json:210` 에서 **"Zou! / Lignes d'Azur 버스"** 로 두 사업자를 병기한다. Villefranche→Èze 는 `line=null`. "광역" 으로 단정할 근거가 없다 |
| Day 11 "Tram 1→15번 환승과 귀환, 각 2회 여정" | **부분 일치** | 왕(트램1+15번)·복(15번) 구조는 일치. 다만 **숙소→Marché de la Libération leg 이 아예 없다**(직선 1.18km, Libération 은 Tram 1 정거장). 트램을 타면 미계상 승차가 생긴다 |
| Day 12 "Nice역 렌터카 인수" | **일치** | walk(숙소→역 1.0km) + car 3구간 · 시내 교통권 사용 0 |

### "두 사람 약 6회" 는 가정 3개 위에 서 있다

```
Day 7 각 1회 = 2      Day 11 각 2회 여정 = 4      합 6
```

성립 조건은 **① Day 10 버스 2구간이 전부 광역(ZOU) · ② Day 11 시장 접근이 도보 · ③ Day 11 환승이 무차감** 셋이 모두 참일 때다.
①은 데이터가 "Lignes d'Azur" 를 병기해 반증되고, ②는 leg 자체가 없어 확인 불가다. 둘 중 하나만 어긋나도 **2인 기준 8회**가 된다.

또 `howToUse` 안에 긴장이 있다 — "환승 때마다 인원수만큼 검증한다"(L136)와 "Day 11 환승도 각각 검증하되 74분 안의 **한 여정**으로 사용한다"(L138). 전자를 문자대로 읽으면 Day 11 은 1인 3검증이라 총 8회다.

**그리고 부족분 대응 문구가 없다.** Barcelona 는 재검증 NOTE-4 를 받아 "두 사람이 4구간을 타면 T-familiar 8회를 모두 쓴다. 이후 추가 승차는 단일권으로 보탠다" 를 넣었는데, **Nice 블록에는 대응 문장이 없다.** Multi voyages 는 재충전이 가능하므로 한 줄이면 해결된다.

---

## 4. 시내권 · TER · ZOU 경계

경계 설정 자체는 옳다 — Day 9 TER 를 시내권과 분리했고, Day 12 를 "공항 왕복권 소진할 귀환 없음" 으로 정확히 짚었다(확정 예약이 Nice-Ville 역 인수이므로 맞다).

문제는 **Day 10 한 곳에 몰려 있다.** TER 3구간은 명확하나 버스 2구간의 사업자·노선·정류장이 셋 다 미확정이고, 그 위에 "광역" 이라는 단정이 얹혀 있다(B1).

---

## 5. 화면 · 회귀 결과

| 검사 | 기저 `527c1c4c` | 브랜치 `15a34e63` | 판정 |
|---|---|---|---|
| `tests/test_stay_transport_guards` | 7 | **11 passed** | Nice·resources 4건 추가 |
| `build/site.py` | 통과 | 통과 (356쪽) | — |
| `build/viewport_check.py` | 통과 | **통과** | 가로 오버플로 0 · 44pt · 11px |
| `build/ux_check.py` · `content_audit` · `pwa_check` | 0 | **0 · 0 · 0** | — |
| `[G1]` / `[G2]` | 1건 / 381건 | 1건 / **380건** | 기저 · G2 1건 개선 |
| 콘솔 오류(390px·1024px) | — | **0건** | — |

Nice 지역 페이지 실측: 상품 카드 3장(Multi voyages · La Carte · Aéro), 이용법 4줄, 예외 3줄, Day 7~12 링크 6개 전부 정상, 공식 출처 5건 접기, 교통 지도 블록의 `PDF 열기`(103×44) · `공식 최신판`(114×44) 둘 다 44pt 충족. 모바일에서 결론→상품→이용법→예외→Day→출처→자료 순서가 그대로 읽힌다.

**폐기 요금은 화면에 없다** — `€1.80` · `1일권 €5` 는 `guide/nice.html` 과 사이트 전체에서 **0건**이다.

---

## 6. 비차단 지적

| # | 내용 |
|---|---|
| N1 | **챕터에 폐기 요금이 3곳 남아 있다.** `06_Nice_..._v2.0.md` L240 "단발권 €1.80", L264 "단발권 €1.80(**1시간** 내 환승), 1일권 €5 … **1일권 €5 가 유리하다**", L275 "(단발 €1.80 … 1일권 €5.00) \| **검증 완료**". L81 의 새 결론("1일권은 사지 않는다")과 **같은 파일 안에서 정면 충돌**하고 환승 시간도 74분이 아닌 1시간이다. 렌더되지 않아 차단은 아니나 편집자가 그대로 믿을 자리다 |
| N2 | **그 가드가 공회전한다.** `tests/…:151` 이 찾는 `"단발권은 €1.80"` · `"1일권(€5.00)"` 는 챕터에 **0건**이고, 실제 남은 표기는 `단발권 **€1.80**` 형태로 **3건**이다. 즉 초록불이 잔존을 보증하지 않는다. Barcelona 가드도 같은 리터럴 방식이지만 그쪽은 잔존 0건이 실증됐다 |
| N3 | `test_nice_public_transit_matches_daily_cards` 는 이름과 달리 **daily-card 를 한 번도 읽지 않는다.** 렌더 문자열 5개와 링크 6개 존재만 본다. 값(요금·횟수·모드) 대조는 스위트 전체에 없다 |
| N4 | Day 10·11 의 leg 에 `line` 이 비어 있다(602/15/트램1 이 `duration` 산문에만 있다). 승차 횟수를 기계로 셀 수 없는 근본 원인이다 |
| N5 | **렌더되는 「추천 체류 리듬」이 "다음 날 아침 공항 렌터카를 인수해" 라고 한다**(L71). 확정 예약은 Nice-Ville 역 인수이고 챕터 L83 도 그렇게 적었다. Aéro 왕복권 비추천 논리가 "공항 귀환 없음" 에 기대므로 이 문장은 결론과도 어긋난다. 요청서가 Hertz 사항을 차단 사유에서 제외했으므로 차단하지 않으나, 화면에 나가는 모순이라 기록한다 |
| N6 | Barcelona 재검증 NOTE 6건 중 **3건 반영**(N1 메시지·N4 상한초과·N5 제목조건), **3건 미반영**(day-02 leg 표기·rebase·). Nice 블록은 그 교훈을 상속하지 않았다 — NOTE-4 대응 문장이 없다 |

---

## 7. 다음 도시 확장 전 권고

1. **leg 에 `line` 을 채우고 승차 횟수를 기계로 센다.** Nice 에서 6회 산술이 흔들린 이유가 전부 여기서 나온다. Aix·Avignon·Lyon 은 노선이 더 얽혀 있어 사람이 세면 반드시 어긋난다.
2. **정류장 이름을 노선 공식 표기로 쓴다.** "Villefranche" 와 "Col de Villefranche" 의 차이가 하루를 통째로 날린다.
3. **배차가 희소한 노선은 편수를 반드시 싣는다.** 하루 6편짜리를 시간표 없이 안내하면 계획이 아니라 도박이다.
4. **stale 가드를 리터럴에서 값·패턴으로 바꾼다.** `€1.80` 같은 값 자체를 금지어로 두어야 표기가 바뀌어도 잡힌다.
5. **자료 동봉 정책을 사진과 같은 기준으로 통일한다.** 라이선스·권리자·재배포 가부를 필수 필드로 두고 빌드가 거부하게 한다.
6. **부족분 대응 문구를 도시마다 넣는다.** "모자라면 어떻게 보태는가" 는 승차 추천의 필수 구성요소다.

---

## 요약

| 축 | 결과 |
|---|---|
| 공식 사실 | **8/8 일치** — 강점 |
| 추가 확인 | 602 정류장 오표기(**차단**) · Day 11 소요시간 공식 근거 없음 |
| 일정 정합 | 4 일치 · Day 10 불일치 · Day 11 미모델링 승차 |
| 승차 산술 | 가정 3개 중 2개 무근거 · 부족분 대응 없음 |
| 화면·회귀 | **신규 회귀 0건** — 강점 |
| 자료 권리 | 기록 부재(**차단**) |

차단 2건은 모두 국소 수정으로 해소된다. 해소 후 재검증을 권고한다.
