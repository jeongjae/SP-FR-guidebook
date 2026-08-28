---
title: "RS01 Phase 1 — 정본 골격 게이트 로그"
version: "1.0"
created: "2026-08-28"
status: "통과 (예정된 실패 1건 잔존 — Phase 4 범위)"
---

# Phase 1 게이트 결과

빌드는 클라우드 클론(main 23443f8, 로컬 정본과 해시 일치 확인)에서 실행·검증했고,
변경분 12개 파일을 로컬 저장소에 반영했다.

## 변경 파일 (12)

| 파일 | 변경 |
|---|---|
| `source/CURRENT/10_Core/itinerary.json` | verdon(Moustiers, 9/9~9/10, 1박) 삽입 — nice 다음 위치(거점 판정 순서 때문에 필수). aix 9/10~9/14 · luberon 9/14~9/16 · avignon 9/16~9/20 4박. 연속성·박수 42 검증 통과 |
| `source/CURRENT/10_Core/regions.json` | verdon 지역 엔트리 (숙소 미정 명시) |
| `data/region-consolidation.json` | consolidated + layerTitles.verdon |
| `build/promote_regions.py` | CHAPTER_FILES에 verdon → 06B |
| `build/content_guard.py` | CHAPTER_FILES · region_name_map · 카드 8→9 |
| `build/model.py` | 지역 수 검증 8→9 |
| `data/media-catalog.schema.json` | regionSlug enum에 verdon |
| `data/place-facts.schema.json` | region enum에 verdon |
| `source/CURRENT/20_Regional_Chapters/06B_Verdon_Moustiers_v1.0.md` | 신규 — rc-region-v1 골격 초안. 미검증 운영정보 전부 pending, 숙소 미정 |
| `source/ASSETS/89_Commercial_City_Experience_Cards_v1.0.md` | Verdon 카드 추가 (9개) |
| `source/CURRENT/20_Regions/verdon.md` | 빌드 파생물 (자동 생성) |
| `FCR02_FOOD_COMPLETENESS.json` | 빌드 리포트 (자동 갱신) |

## 빌드가 드러낸 필수 슬롯 (오류 순서대로)

1. `model.py` 지역 수 하드코딩 8 → 수정 완료
2. `content_guard.py` 카드 수 8·region_name_map → 수정 완료
3. 06B 챕터 부재 → 골격 생성 완료
4. Commercial Card 9번째 → 추가 완료
5. 원고 흔적 가드 — 골격 초안의 제작단계 표현 2건 → 문구 수정 완료

## 통과한 가드

지역 9쪽 렌더 · 확정 사실 토큰 45건 생존 · Phase 9 상용편집 · 사진 연결 0건 ·
조사 종결 0건 · 원고 흔적 0건(verdon 포함 9지역) · 리다이렉트 176쪽 · PWA 977파일

## 예정된 잔존 실패 (Phase 4에서 해소)

```
지역 구조 가드 실패:
  avignon: 이 지역과 무관한 Day 링크 — Day 18
```

Day 18(9/15)이 avignon→luberon으로 넘어갔는데 avignon 챕터가 아직 Day 18을
도착일로 서술하기 때문. 챕터 수정(Phase 4) 전까지 빌드는 이 한 건으로 실패하는
것이 정상이다. 이 실패가 사라지면 Phase 4의 avignon 수정이 된 것이다.

## 주의 — 로컬 빌드 시 jsonschema

클라우드는 jsonschema 4.26으로 빌드했다. 로컬 파이썬의 jsonschema가 구버전이면
`Draft202012Validator` 오류가 난다 → `pip install --upgrade jsonschema`.
