---
title: "RS01 최종 검증 QA — Verdon 1박 삽입 일정 조정"
version: "1.0"
created: "2026-08-28"
scope: "Phase 0~7 전체"
verdict: "전 게이트 통과 (9/9)"
---

# RS01 최종 검증 QA

지시서(`RS01_VERDON_RESCHEDULE_INSTRUCTION_v1.0.md`) §2.8의 게이트를 실행한 기록이다.
실행 환경: 클라우드 클론 (main 23443f8 기점 + RS01 커밋), 2026-08-28.

## 게이트 결과

| # | 게이트 | 결과 | 근거 |
|---|---|---|---|
| G1 | 빌드 전체 | **PASS** | 410쪽 · 검색 색인 215건 · 전 가드(원고 흔적·사진·조사·구조·Phase 9) 통과 |
| G2 | 박수·일수·지역 | **PASS** | 42박 · 43일 · 지역 9개 |
| G2b | 숙박 연속성 | **PASS** | 전 구간 체크아웃 = 다음 체크인 |
| G4 | Day↔장소 교차 | **PASS** | daily-cards place_ref ↔ place-days.json 불일치 0건 |
| G5 | 하드 앵커 | **PASS** | 렌터카 9/9 09:00 Nice-Ville 인수 · 9/17 18:30 이전 Avignon TGV 반납 · TGV 12176 10:22 · Aix 9/10~9/14 확정 |
| G6 | 미확정 숙소 표시 | **PASS** | Moustiers·Gordes·Avignon 숙소 confirmed 표기 0건 (candidate 유지) |
| G7 | 요일 제약 | **PASS** | Saint-Rémy 수(9/16=Day 19) · Gordes 화(9/15=Day 18) · Aix 토(9/12=Day 15) · Lacoste 월(9/14=Day 17) |
| G8 | 구일정 잔존 | **PASS** | 정본 계층(source/CURRENT + daily-cards)에서 "Avignon 5박"·"목요시장" 등 금지 패턴 0건 |
| G9 | 테스트 | **PASS** | 142 passed · 380 subtests |

재발 방지: G8의 금지 패턴은 `data/decisions.json` DEC-RS01-A~C에 등재되어
빌드 가드(G5 guard_decisions)가 상시 감시한다 (`also_check_daily_cards` 포함).

## 알려진 한계 (게이트 밖)

- **신규 좌표 근사치**: Point Sublime·Galetas·Castellane·Route des Crêtes 좌표는
  OSM 지오코딩 재확인 전 근사값이다. daily-cards `needsReview`에 등재됨.
- **구간 실주행 미검증**: Grasse→Moustiers, Moustiers→Aix 구간별 시간·거리는
  공식 총계(Nice 2h15·Aix 1h45) 외 재확인 표기 상태다.
- **9월 운영 미확인**: Moustiers 식당 수요일 저녁, Point Sublime 9월 주차 요금,
  호수 물가 활동, La Palud 점심 — `verify-queue.csv` P0/P1 등재됨.
- **과거 감사 기록 36건**: AV01·AX01·EX01(구판)·FCR 계열 QA는 시점 기록으로
  보존한다. 현재 상태 정본은 이 문서와 EX-01 재생성분이다.

## 사용자 액션 (문서 밖 실물 세계)

1. **Moustiers 9/9 1박 숙소 확보 — 최우선** (내일 출국)
2. Gordes 9/14~9/16 2박 확보
3. Avignon 9/16~9/20 4박 확보
4. Sénanque 9/15(화) HistoPad 회차 재예매 (9/14 확인분 무효)
5. Atelier des Lauves 9/12(토) 회차 예약
6. 칼랑크 유람선 9/13(일) 48시간 전 예약 · Chez Gilbert 일요일 영업 재확인
7. Aix 9/10~9/14 날짜 변경 확인서 보관

## 종결

RS01 콘텐츠 작업은 이 문서로 종결한다. 이후 남는 것은 위 사용자 액션과,
숙소 확정 시의 동기화(각 챕터 "확정 후 동기화" 절 참조)뿐이다.
