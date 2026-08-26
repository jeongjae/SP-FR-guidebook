# 116. Phase 10 Official-Source Fact Verification Register v1.0

**검증일:** 2026-08-04 · **2차 검증 2026-08-14 (F024–F036, 콘텐츠 품질 R1)** · **3차 검증 2026-08-15 (F037–F042, R4 식당 영업일)**
**원칙:** 공식 운영기관·지자체·국립공원·관광기관의 현재 웹페이지를 우선한다.

## 상태 정의

| 상태 | 의미 |
|---|---|
| VERIFIED | 일정일에 적용 가능한 운영·방문정보 확인 |
| VERIFIED_CURRENT | 현재 확인됐으나 예약일 가격은 예약화면에서 다시 확정 |
| CORRECTED | 기존 문구 또는 숫자를 수정 |
| CONFLICT_RECHECK | 동일 기관 페이지 간 차이가 있어 날짜별 화면 재확인 필요 |
| DATE_GATE | 일정일 전날 또는 당일에만 확정 가능한 정보 |

## 공식자료 검증표

| ID | 지역 | 장소 | 항목 | 상태 | 확인내용 | 공식출처 | 조치 |
|---|---|---|---|---|---|---|---|
| F001 | Barcelona | Sagrada Família | 운영시간 | VERIFIED | 4–9월 월–금 09:00–20:00, 토 09:00–18:00, 일 10:30–20:00. 특별행사로 변경 가능. | [공식](https://sagradafamilia.org/en/schedules-how-to-get) | 8/29 도착 후 8/30 방문 전날 재확인 |
| F002 | Barcelona | Sagrada Família | 티켓 | CORRECTED | 공식 웹사이트 온라인 구매만 가능. 타워 포함 일반권은 현재 €36 표시. 기본권 가격은 실제 예약화면에서 확정. | [공식](https://sagradafamilia.org/en/tickets-individuals) | 기존 ‘기본권 약 €26’ 고정표현 제거 |
| F003 | Barcelona | Sant Pau | 운영·요금 | VERIFIED | 4–10월 매일 09:30–18:30, 마지막 입장 30분 전. 자유관람 45–60분. 일반 €18(14시 이전), €17(14시 이후). | [공식](https://santpaubarcelona.org/en/visita/visita-lliure/) | 8/30 현장 동선에 반영 |
| F004 | Barcelona | MACBA | 무료시간 | VERIFIED | 여름 목·금·토 18:00–20:00 무료, 매월 첫째 일요일 무료. 전시일정과 정규 운영시간은 당일 페이지 확인. | [공식](https://www.macba.cat/en/plan-your-visit/free-entrance-and-discount-admission/) | 8/31 월요일 방문의 정규 개관 여부 48시간 전 확인 |
| F005 | Barcelona | Cau Ferrat·Maricel | 운영·요금 | CONFLICT_RECHECK | 공식 Schedule 페이지는 4–10월 화–일 10:00–19:00, 월 휴관. 다른 공식 여름 안내는 7–9월 20:00까지 표기. 통합권 €12. | [공식](https://museusdesitges.cat/en/schedule) | 9/1 공식 티켓화면에서 최종 확인 |
| F006 | Girona | Girona Walls | 운영시간 | VERIFIED | 9–5월 08:00–21:00. 6–8월 08:00–23:00. | [공식](https://www.girona.cat/turisme/eng/monuments_muralla.php) | 9/1·9/3 일정과 일치 |
| F007 | Girona | Historic City | 역사 | VERIFIED | 로마 Força Vella와 14–15세기 중세 확장 성벽의 두 방어체계가 핵심. | [공식](https://www.girona.cat/turisme/eng/monuments.php) | 지역해설 유지 |
| F008 | Aix/Cassis | Calanques National Park | 접근·요금 | CORRECTED | 공원 입장은 무료. 연중 개방이 원칙이나 화재위험 red day에는 폐쇄. 6/1–9/30 접근금지 가능, 일부 도로 차량통제. | [공식](https://www.calanques-parcnational.fr/en/frequently-asked-questions) | Day 14 전날·당일 My Calanques 확인 |
| F009 | Aix/Cassis 대안 | Calanques National Park | 안전 | VERIFIED | 육상접근 조건은 매일 변동. 충분한 물·장비가 필요하며 인기 해변에는 상점·급수·화장실·쓰레기통이 없음. | [공식](https://www.calanques-parcnational.fr/en/prepare-your-visit-calanques) | 기본 일정이 아닌 Cassis 대안 안전게이트로 유지 |
| F010 | Paris | Notre-Dame | 입장·예약 | CORRECTED | 성당 입장은 100% 무료. 공식사이트 외 유료티켓 판매자는 비공식. 예약은 선택이나 권장, 보통 전날·이틀 전·당일 슬롯 공개. | [공식](https://www.notredamedeparis.fr/en/visit/reservation-free/) | ‘사전 장기예약’ 표현 금지 |
| F011 | Paris | Notre-Dame | 접근 | VERIFIED | Cité역(M4), Saint-Michel역(M4/RER B·C). 전례가 관광보다 우선. | [공식](https://www.notredamedeparis.fr/en/visit/visitor-reception/) | 9/26 방문 전 예배일정 확인 |
| F012 | Paris | Versailles | 운영 | VERIFIED | 궁전은 월요일 휴관, 화–일 09:00 개장. Trianon은 12:00 개장. 4–10월 정원 유료행사일 존재. | [공식](https://en.chateauversailles.fr/plan-your-visit) | 10/3 토요일 시간지정 필수 |
| F013 | Paris | Versailles | 시간지정 | VERIFIED | Passport 시간지정 입장은 09:00–15:00 매시 슬롯, 예약시간 기준 30분 유효. | [공식](https://en.chateauversailles.fr/passport-timed-entry) | 09:00 슬롯 우선 |
| F014 | Paris | Versailles | 후반입장 가격 | VERIFIED_CURRENT | 고시즌 16:00 이후 Passport 우대가격 €28(EEA €25). 일반 Passport 정확한 가격은 날짜별 예약화면 확인. | [공식](https://ticket.chateauversailles.fr/en/ticketing) | 가격을 고정하지 않고 예약화면 캡처 |
| F015 | Paris | Notre-Dame Treasury | 요금 | VERIFIED | 성당 본당은 무료이나 Treasury는 일반 €12, 할인 €6. 현장판매, 온라인예약 없음. | [공식](https://www.notredamedeparis.fr/en/visit/visit-treasury/) | 본당과 Treasury 요금 구분 |
| F016 | Barcelona | Sitges Museums | 요금 | VERIFIED | Cau Ferrat+Maricel 일반 통합권 €12, Stämpfli 포함 결합권 €17. | [공식](https://museusdesitges.cat/en/fees) | 9/1 이동일은 €12 통합권 범위만 검토 |
| F017 | Barcelona | Sant Pau | 관람동선 | VERIFIED | Hypostyle Hall→지하터널→Sant Salvador Pavilion 순으로 병원역사와 Domènech i Montaner를 이해하는 공식 동선. | [공식](https://santpaubarcelona.org/en/visites/) | Sagrada 이후 60분 관람 |
| F018 | Barcelona | MACBA Library | 운영 | VERIFIED | 도서관은 월–목 10:00–19:00, 금–일 휴관. 8월 휴관, 9/1–15는 10:00–18:00 특별시간. | [공식](https://www.macba.cat/en/library/) | 8/31에는 8월 휴관이므로 도서관 일정 제외 |
| F019 | Aix/Marseille | Mucem | 운영 | VERIFIED_CURRENT | 공식 FAQ 기준 9/1–11/2는 10:00–19:00, 화요일 휴관, 전시실 마지막 입장 폐관 45분 전. 9/12 토요일 일정과 충돌 없음. J4와 Fort Saint-Jean 연결 동선은 현장 통제 가능. | [공식](https://mucem.org/questions-frequentes/) | 전날 운영·전시실·보행교 통제 재확인 |
| F020 | Aix/Marseille | TER / Ligne 50 | 교통 | DATE_GATE | Day 15 기본 교통은 Aix Centre–Marseille Saint-Charles TER이며 L50은 철도 이상 시 fallback. 실제 9/12 시각·승강장·공사·파업은 고정정보가 아님. | SNCF Connect · [Métropole Mobilité](https://www.lametropolemobilite.fr/) | 전날 공식 경로검색과 당일 알림 확인 |
| F021 | Avignon/Arles | Arènes d’Arles | 운영 | VERIFIED_CURRENT | Arles 관광청 현행 안내상 9/14–30 매일 09:00–19:00. 행사·JEP로 동선이 바뀔 수 있음. | [공식](https://www.arlestourisme.com/fr/d%C3%A9tails.html?culture=L%27+Amphith%C3%A9%C3%A2tre+romain&ident=5538604%3F%3F) | 9/19 출발 전 공식 페이지 재확인 |
| F022 | Avignon/Arles | Cloître Saint-Trophime | 운영 | VERIFIED_CURRENT | Arles 관광청 현행 안내상 9/14–30 매일 09:00–19:00. Théâtre antique와 함께 볼 때 Saint-Trophime 또는 Fondation 중 하나만 선택. | [공식](https://www.arlestourisme.com/fr/d%C3%A9tails.html?culture=Clo%C3%AEtre+Saint+Trophime&ident=5538418) | 9/19 운영·마지막 입장 재확인 |
| F023 | Avignon/Arles | Journées européennes du patrimoine | 운영·행사 | DATE_GATE | 2026 공식 날짜는 9/19–20. 공식 프로그램에 Théâtre antique와 Arènes의 무료 플래시 투어가 게시되어 있으나 회차·집합장소·예약·혼잡은 변동 가능. | [공식](https://journeesdupatrimoine.culture.gouv.fr/w/377623/evenement/19064472/visite-flash-du-theatre-antique) | Arènes 프로그램도 공식 포털에서 함께 확인하고 모든 세부는 **출발 전 재확인** |
| F024 | Barcelona | Sagrada Família | 요금 | VERIFIED_CURRENT | Basilica €26 · 가이드 €30 · 타워 €36 · 가이드+타워 €40 (2026-08-14). | [공식](https://sagradafamilia.org/en/prices) | 예약화면에서 최종 확정 |
| F025 | Barcelona | MACBA | 운영·요금 | VERIFIED | 여름(6/25–9/24) 월·수·목·금·토 10:00–20:00, 일 10:00–15:00, 화 휴관. 온라인 €13.50 · 현장 €15. 8/31 월요일 개관. | [공식](https://www.macba.cat/en/plan-your-visit/) | 8/31 방문 48시간 전 전시실 폐쇄 확인 |
| F026 | Barcelona | Recinte Modernista de Sant Pau | 운영·요금 | VERIFIED | 4–10월 매일 09:30–18:30(월요일 개관). 자율관람 14시 전 €18 · 14시 이후 €17. 8/30 14:30 입장은 €17 요율. | [공식](https://santpaubarcelona.org/en/prepara-la-teva-visita/) | 원고에 없던 운영·요금을 추가 |
| F027 | Sitges | Museu del Cau Ferrat · Maricel | 요금 | CORRECTED | 통합권 일반 €12 · 감면 €8 · 초감면 €6. **원고의 €6 은 초감면 요율이었다** — 일반 €12/인, 2인 €24 로 정정. | [공식](https://museusdesitges.cat/ca/tarifes) | 예상 현지비용표 총계 함께 정정 |
| F028 | Aix | Musée Granet | 운영·요금 | VERIFIED | 2026-11-01 까지 화–일 10:00–18:00, 매표 17:30, 월 휴관. 일반 €14·감액 €12이며 Paul McCartney 《Eyes of the Storm》이 기본 입장에 포함된다. Granet XXe는 별도 site. | [공식](https://www.museegranet-aixenprovence.fr/en/practical-informations-1/opening-hours-and-admissions) | 9/10 방문 전 재확인 |
| F029 | Luberon | Village des Bories | 운영·요금 | VERIFIED | 9월 매일 09:00–19:00, 마지막 입장 마감 30분 전, 성인 €8. | [공식](https://luberon.fr/tourisme/les-sites-touristiques/monuments/annu+village-des-bories+1712.html) | 9/15 방문 전 재확인 |
| F030 | Luberon | Sentier des Ocres | 운영·요금 | CORRECTED | 9월 09:30–18:30 개방, 탐방로 퇴장 19:00, 성인 €3.50. 원고의 '09:30–19:00 · 마지막 입장 18:30' 표현을 공식 표기에 맞춰 정정. | [공식](https://roussillon-en-provence.fr/decouvrir-2/sentier-des-ocres/) | 우천·산불 시 폐쇄 당일 확인 |
| F031 | Paris | Musée du Louvre | 운영·요금 | VERIFIED | 화요일 휴관. 월·목·토·일 09:00–18:00, 수·금 21:00. 마지막 입장 마감 1시간 전. 비EEA €32 · EEA €22. | [공식](https://www.louvre.fr/en/visit) | 9/28 시간지정권 예약 |
| F032 | Girona | Girona Cathedral | 요금 | VERIFIED_CURRENT | 대성당+Sant Feliu 통합권 일반 €7.50, 미술관 포함 €12. | [공식](https://tickets.catedraldegirona.cat/en) | 9/1 축소안 실행 시 현장 확인 |
| F033 | Paris | Musée de l’Orangerie | 휴관 | CORRECTED | **화요일 휴관.** 9/29(화)에 'Orsay 또는 Orangerie 택1' 로 적혀 있던 선택지를 Orsay 고정으로 정정하고 Orangerie 는 10/3 후보로 이동. | [공식](https://www.musee-orangerie.fr/en/visit-orangerie) | 10/3 방문 시 재확인 |
| F034 | Aix | Atelier des Lauves (Cézanne) | 운영·요금·예약 | CORRECTED | 2026-07-04~09-30 매일 09:00–18:00(마지막 관람 17:00). 자율관람은 11:30부터 1시간 €9.50, 가이드 1시간 30분 €12. 정원 제한으로 사전 예약 강력 권장, slot 보장은 예약 시. | [공식](https://www.aix.fr/incontournables/atelier-cezanne) | ACTION REQUIRED — 9/10 시간지정 예약 |
| F035 | Paris | ParisLongchamp (Arc) | 접근 | DATE_GATE | Porte d’Auteuil·Porte Maillot 에서 경마장행 **무료 셔틀** 운행 확인. 첫차·배차·막차는 회차 공지에서만 확정된다. | [공식](https://www.france-galop.com/en/content/qatar-prix-de-larc-de-triomphe-worlds-greatest-horse-race) | 10/4 당일 공지 확인 |
| F036 | Barcelona | Hertz (스페인 렌터카) | 국경운전 | VERIFIED | 스페인 밖 운행 시 크로스보더 요금이 부과되고, **신고하지 않으면 제3자·CDW·도난·SuperCover 가 무효**가 된다. 프랑스는 허용 국가. | [공식](https://www.hertz.com/rentacar/reservation/reviewmodifycancel/templates/rentalTerms.jsp?KEYWORD=DRIVINGRESTRICTIONS&EOAG=MADT50) | 9/1 인수 창구에서 프랑스 주행 신고 |
| F037 | Lyon | Daniel et Denise Créqui | 영업일 | CORRECTED | 월–금 12–14 · 19–22, **토·일 휴무.** 원고의 '화요일 휴무' 리스크는 반대로 틀린 정보 — 9/22(화) 예약 정상. | [공식](https://danieletdenise.fr/) | 예약 시 지각정책 확인 |
| F038 | Lyon | Café Comptoir Abel | 영업일 | CORRECTED | **매일 영업** (월–목 12–14 · 19:30–22 등). 원고의 '월요일 휴무' 우려 해소 — 9/21(월) 예약 정상. | [공식](https://www.maisonabel.fr/maison-abel/le-cafe-comptoir-chez-abel/) | 예약 시 취소정책 확인 |
| F043 | Luberon | La Récréation | 영업·요금 | VERIFIED | 2026 연중 등록, 성수기 7일 운영, 점심 12:00–14:00. à la carte €22–26·성인 메뉴 €37.50–38.50·plat du jour €22. 9/13 12:15 실제 좌석은 미확인. | [공식 관광청](https://www.provenceguide.com/restaurants/luberon/la-recreation/provence-2997991-1.html) | ACTION REQUIRED — 9/13 좌석 확인; 실패 시 Lourmarin 현장 식사 |
| F044 | Luberon | Bistrot Le 5 | 영업일 | CORRECTED | 공식 사이트에 **월요일 휴무**, 화–일 11:30–00:00로 표시. 9/14(월) Day 17 점심으로 의존하지 않음. | [공식](https://bistrotle5.com/) | Roussillon / Ménerbes 간단식 / Gordes 방향 복귀 fallback |
| F045 | Luberon | Abbaye Notre-Dame de Sénanque | 9/14 예매 슬롯 | VERIFIED_CURRENT | 2026-08-25 공식 예매 화면에 2026-09-14 HistoPad 15:00·16:00·17:00 회차가 표시됨. 기존 16:00–17:30 창은 16:00 회차와 일치. | [공식 안내](https://www.senanque.fr/en/visits-of-the-abbey-2/) · [공식 예매](https://abbaye-senanque.tickeasy.com/en-GB/) | ACTION REQUIRED — 16:00 HistoPad 예약·오프라인 저장 |
| F046 | Provence | Gordes·Avignon 숙소 | 예약 상태 | ACTION_REQUIRED | Master Tracker Reservations/Accommodation 시트에 Gordes 9/13–15 2박·Avignon 9/15–20 5박 모두 미예약/재확인. 후보명은 확정 숙소로 사용 금지. | `TP_Europe_Travel_Master_Tracker_v1.2.xlsx` | 숙소 확정 후 주소·체크인·주차·연락처·일일 동선 동기화 |
| F047 | Grasse | Usine Historique Fragonard | 운영·예약·접근 | VERIFIED | 20 boulevard Fragonard, 매일 09:00–19:00. 개인 무료 가이드 방문은 예약 불필요·약 30분 간격 현장 출발. 2026 centenary exhibition 6/19–10/18 무료·예약 불필요. | [공장](https://usines-parfum.fragonard.com/usines/usine-historique/) · [특별전](https://www.fragonard.com/en-us/exhibition-fragonard-100ans-2026) | Day 12 정상 13:15 도착일 때만 실행, Parking Indigo CRESP 사용 |
| F048 | Aix | Place Richelme·목요 확장시장 | 운영 | CORRECTED | Richelme 식품시장은 매일 08:00–13:00. 화·목·토 Places Comtales 식품시장, Cours Mirabeau·Forbin·Comtales 직물/공예/브로칸트, Hôtel de Ville 꽃시장. | [공식](https://www.aixenprovencetourism.com/en/shopping/the-provencal-markets/) | ‘Richelme 목요 대형시장’ 표현 제거 |
| F049 | Cassis | Calanques 보트 | 운영·소요시간 | CORRECTED | 매일 기상 허용 시 운항. 공식 소요시간은 3개 1h·5개 1h20·8개 1h50·9개 2h20. Day 14는 Port-Miou·Port-Pin·En-Vau의 3 Calanques 유지. | [공식](https://www.ot-cassis.com/en/explore/the-calanques/the-calanques-by-boat/) | 실제 운항·티켓 CHECK, 8 Calanques로 승격 금지 |
| F050 | Cassis | Parking des Gorguettes | 주차·버스 | CORRECTED | 무료 P+R 연중. Bus 372 centre-ville 연중. Bus 373 Presqu’île는 2026-04-04~11-01 중 방학·주말·공휴일 중심. | [공식 주차](https://www.ot-cassis.com/en/practical-info/parking-parking/) · [Gorguettes](https://www.ot-cassis.com/imaginez/avez-vous-pense-au-parking-relais-des-gorguettes/) | 9/11 금요일 373 운행을 가정하지 않고 372를 기본 사용 |
| F051 | Marseille | Vieux-Port fish market | 운영·위치 | CORRECTED | Quai de la Fraternité에서 매일 아침 운영. 공식 안내의 시간 표기는 07:30–12:30 또는 08:00–13:00이며 날씨·계절에 따라 규모 변동. | [공식](https://www.marseille-tourisme.com/decouvrez-marseille/traditions/marche-aux-poissons-marseille/) | ‘토요 어시장’ 표현 제거 |
| F039 | Sitges | La Zorra | 영업일 | CONFLICT_RECHECK | 공식 사이트 매일 13:00–16:30 · 20:30–23:00, 일부 포털 월요일 휴무 표기 — 상충. 방문일 9/1(화)은 어느 기준으로도 영업일. | [공식](https://restaurantelazorra.com/horario-y-contacto/) | 예약 확정 문자로 해소 |
| F040 | Barcelona | Bar Cañete | 영업일 | VERIFIED | 월–토 13:00–24:00, **일요일 휴무** — 8/31(월) 점심 정상. | [공식](https://barcanete.com/en/bookings/) | 온라인 예약 우선 |
| F041 | Barcelona | La Paradeta Sagrada Família | 영업일 | VERIFIED | 일요일 13:00–16:00 영업 · 일 저녁·월요일 휴무 — 8/30(일) 점심 정상. 예약 없음(줄서기). | [공식](https://www.laparadeta.com/en/seafood-restaurants/) | 개점 직전 도착 |
| F042 | Barcelona | Bodega Joan | 영업일 | VERIFIED | 매일 영업 — 점심 12:00–18:00 · 저녁 18:00~. 8/29·30 저녁 후보 정상. | [공식](https://www.bodegajoan.com/en) | 예약 선택 |

## 범위와 한계

- 51개 장소의 역사·문화 설명은 Phase 9D에서 공식링크와 함께 정리했다.
- Phase 10에서는 일정에 영향을 크게 주는 시간·요금·휴관·접근·예약 조건을 우선 검증했다.
- 식당, 숙소, 공연, 축구, 실제 열차·항공은 예약정보가 없으므로 Phase 8B가 완료될 때까지 확정하지 않는다.
- Calanques 화재통제, 날씨, 파업, 열차운행은 고정정보가 아니므로 전날·당일 게이트로 관리한다.
