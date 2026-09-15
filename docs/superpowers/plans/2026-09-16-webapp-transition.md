# SP-FR 가이드북 → 편집 가능한 모바일 웹앱 전환 계획

## Context

- 현재 사이트(jeongjae.github.io/SP-FR-guidebook)는 415쪽 정적 HTML. 모든 변경이 `source/`·`data/` 편집 → Python 빌드 → 가드 → CI 배포(푸시→라이브 ~3.5분)를 거쳐, 여행 중 폰에서 일정·예약을 고치기 어렵다. 오늘 = Day 19/43, 잔여 24일.
- 사용자 결정: ① 편집 범위 = **일정·시간표 / 예약·상태 / 메모·기록 / 장소·본문 전부** ② **IndexedDB 기반 모바일 웹앱**(로컬 우선·오프라인 편집) ③ **여행 중 바로 전환하되 기존 정적 사이트는 그대로 유지**, 웹앱은 새 사이트로 병행 ④ 동기화·인증 인프라는 제안 필요 → **GitHub 전용(PAT) 권장** (아래).
- 지켜야 할 자산: 빌드 가드 스위트(43일 전수·날짜 연속성·place_ref·시장 요일·확정 사실 생존), git=정본, 완전 오프라인, 런타임 서드파티 의존성 0.
- 조사 확정 사실: site/ 에 구조화 데이터 미공개(빌드 전용) · 로컬 상태 전례는 `spfr_paris_museum_booking_state`(canonical 위 오버레이, app.js L873–1087) · 메인 SW 는 전 파일 해시 버전 + 옵트인 85.6 MiB 전체 저장·델타 없음(사소한 변경도 오프라인 사용자는 1001파일 재다운로드) · 사진이 62 MB 지배, JSON/HTML 은 작다 · 배포는 freshness 게이트로 직렬화, 푸시→라이브 3~3.5분.

## 권장 아키텍처 (확정안)

**같은 저장소·같은 오리진.** 새 최상위 `app/` 디렉터리를 빌드가 `site/app/` 으로 그대로 복사 + `build/export_app_data.py` 가 정본 데이터를 JSON 스냅샷(~2 MB)으로 내보낸다. 앱은 **바닐라 JS 해시 라우팅 SPA**, **자체 서비스워커(scope `/SP-FR-guidebook/app/`)**, **IndexedDB = 로컬 정본**(불변 스냅샷 store + append-only 편집 이벤트 저널). 의존성 0 유지(자작 ~100줄 `idb.js`, ~80줄 `md.js`).

**동기화 = GitHub 전용 (권장).** 폰마다 fine-grained PAT(이 저장소만, Contents R/W만, 만료 ~2026-10-25) → 기기별 저널 `data/field-edits/journal-<deviceId>.ndjson` 을 Contents API 로 append → 새 워크플로 `apply-edits.yml` 이 `scripts/apply_field_edits.py` 로 이벤트를 정본 파일에 접어 넣고 **기존 가드 전체를 CI 에서 실행, 통과분만 main 커밋** → pages.yml 이 정적 사이트+스냅샷 재빌드. 거부된 이벤트는 삭제하지 않고 CI 소유 `data/field-edits/state.json` 에 사유와 함께 기록, 앱 `#/sync` 화면에 그대로 노출("수정 후 재제출" 버튼).
- 선택 이유: 운영 부담 0(여행 중 새로 돌볼 서버 없음), git·가드가 정본으로 유지되어 **폰이 배포를 깨뜨릴 수 없음**, 기기별 저널이라 SHA 경합 없음. 단점 수용: PAT 폰 저장(범위·만료 제한, 분실 시 즉시 revoke), 정본 수렴 ~4–6분(로컬 우선이라 편집 폰은 즉시 반영, 상대 기기 저널을 직접 읽는 fast-path 로 수 초 내 상호 가시성).
- 폰에서 정본 파일 직접 커밋은 배제: 두 기기의 파일 SHA 경합, 가드(Python)를 클라이언트가 사전 검증 불가 → main 오염 위험, 감사 추적 없음.

## 데이터 흐름

```
정본(git main: daily-cards·itinerary·30_Places·booking-overrides·field-notes)
  ─pages.yml(빌드+가드)→ site/ (기존 415쪽) + site/app/ (앱+스냅샷 JSON)
  ←apply-edits.yml(apply_field_edits.py: 이벤트 접기→가드→통과분만 커밋)─
폰(2대): IndexedDB[snapshot ⊕ events] → 즉시 렌더 → 온라인 시 저널 push
  → CI 적용 → 다음 스냅샷 pull 로 확정 (pending→pushed→applied|rejected)
```

## IndexedDB 스키마 (DB `spfr_app` v1)

- `snapshot` (key: "trip"|"day-NN"|"places-index"|"places-<region>"|"bookings") — pull 시 통째 교체, 편집으로 절대 변형하지 않음.
- `events` (id=ULID; 인덱스 entity/status/ts) — `{deviceId, author, ts, seq, entity{kind,key}, op, payload, status, rejectReason}`. op: `set-field·add-stop·remove-stop·move-stop·set-day-meta·set-booking·check-action·set-visited·note·prose-set-section·add-place`. 구조 op 는 인덱스가 아니라 **앵커 기반**(`after "saint-remy"`) — 두 기기 동시 편집 합성 가능.
- `peerEvents` — 상대 기기 저널 미러(선택 fast-path). `meta` — deviceId·PAT·커서.
- 뷰 = `materialize(snapshot, events∪peerEvents)`. 이벤트 로그 방식이라 undo·거부 복구·수렴이 공짜.

## 적용(서버측) 병합 규칙 — `scripts/apply_field_edits.py`

`(ts, deviceId, seq)` 전순서 정렬 → 같은 필드 충돌 LWW(진 값은 state.json 에 보존), 삭제 vs 필드수정 충돌은 삭제 승·수정 거부(`stop-removed`), 본문 섹션 충돌 LWW+패자 markdown 보존. 가드 실패 시 엔티티 단위로 이등분 재시도해 위반 이벤트만 rejected 처리 — **main 은 항상 가드 green 커밋만 받는다**. 자기 커밋 재트리거는 pending 0 → no-op (멱등).

## 만들 파일 / 고칠 파일

신규 — 앱 (`app/` → `site/app/`): `index.html` · `app.css` · `manifest.webmanifest`(별도 설치형, scope `./app/`) · `sw.js`(앱 셸+스냅샷 프리캐시 ~2 MB; `../assets/` 사진은 cache-first + 오리진 전역 `caches.match()` 로 메인 SW 의 85 MiB 캐시 재활용) · `js/`: `main·router(#/today·#/day/NN·#/place/<slug>·#/bookings·#/search·#/sync·#/settings)·db·idb·state(materializer)·events·sync·md·views/*·edit/*(stops·times·booking·notes·prose)`.

신규 — 빌드·동기화: `build/export_app_data.py`(manifest.json+trip.json+days/*.json[일일카드 원형 그대로 — `data/daily-cards/schema.json` 공유]+places-index+places/<region>.json[**markdown 원문 유지**, 섹션 단위]+bookings.json ≈ 2 MB) · `build/app_check.py`(스냅샷 스키마+헤드리스 렌더 스모크) · `scripts/apply_field_edits.py` · `.github/workflows/apply-edits.yml` · `data/field-edits/{journal-*.ndjson, state.json}` · `data/booking-overrides.json`(**xlsx 는 동결, 그 위 오버라이드 층** — 기존 canonical-status 오버레이 전례의 일반화) · `data/field-notes.json`.

수정 — 기존(소규모·외과적):
- `build/render.py` write_pwa(~L3368): `app/` 프리픽스를 offline-files.json **과 버전 해시 양쪽에서** 제외 — 앱 수정이 기존 오프라인 사용자에게 85 MiB 재다운로드를 강요하지 않게. **P0 첫 변경이며 offline-files.json 전후 diff 가 수용 기준.**
- `build/pwa_check.py`(L41·L105–120): 같은 제외를 미러(한쪽만 고치면 배포 FAIL).
- `build/site.py`: `app/` 복사 + export 호출. `.github/workflows/pages.yml`: 트리거 경로 `app/**` + `app_check.py` 추가.
- (P3) `build/fact_guard.py`·`content_guard.py`: 클라이언트발 신규 스톱·장소용 `sourceStatus:"field-edit"` 등급 허용(여행 후 회수).

**바꾸지 않는 것:** 기존 415쪽·메인 SW·가드 엄격성·배포 흐름·tracker xlsx.

## 단계별 실행 (반나절 세션 단위, 여행 중 점진 배포)

| 단계 | 내용 | 규모 |
|---|---|---|
| **P0** 스냅샷 공개 | export_app_data + SW 제외 + CI 훅. 기존 오프라인 사용자 무영향 검증 | 0.5~1 세션 (당일) |
| **P1** 읽기 앱 + 안전 편집 | 셸·라우터·IDB·materializer·5개 뷰·앱 SW·설치형. **로컬 전용** 편집: 메모·방문체크·예약 상태·ACTION 체크오프 | 1.5~2 세션 (1~2일) |
| **P2** GitHub 동기화 | PAT 설정 UI·push/pull·apply 스크립트(비구조 op: notes→field-notes, bookings→booking-overrides)·apply-edits.yml·거부 노출·상대 저널 오버레이 | 1.5~2 세션 (3~4일차) |
| **P3** 구조·본문 편집 | 스톱 추가/삭제/순서/시각·하루 재배치→day-NN.json, 가드 field-edit 등급, 장소 본문 섹션 편집·식당 추가→30_Places+명부 | 2~3 세션 (잔여 여행 중 점진; 시각·순서 변경부터) |
| **P4** 여행 후 경화 | PAT 회수·저널 압축/보관·field-notes→여행기 내보내기·가드 예외 회수 | 1~2 세션 |

**향후 2~3일 현실 목표 = P0+P1 완료, P2 대부분** — 편집 범위 4개 중 3개(예약·상태/메모·기록 + 읽기)가 폰에서 돌아간다. P3 완성 전까지 구조적 일정 변경은 기존 노트북 워크플로 병행.

## 검증

- P0: 로컬에서 pages.yml 검사 블록 전체 + `offline-files.json` totalFiles/version 이 P0 이전 빌드와 동일함을 diff 로 확인 + app_check(스냅샷 스키마·manifest 해시).
- P1: app_check 를 Playwright(이미 CI 에 설치됨)로 확장 — `/app/#/today` 가 스냅샷에서 Day 렌더, 이벤트 append→재로드 지속성, 설치성. 수동: 두 폰 비행기모드.
- P2: `apply_field_edits.py` 단위테스트(build/test_validation.py 스타일) — 정상/동일필드 충돌/삭제vs수정/**고의 가드 위반(시장 요일 오류)→ 거부 + main 청정** 4종 + 실기기 왕복 1회.
- P3: 두 기기 구조 op 임의 교차 수렴 property 테스트 + 날짜 연속성 가드 케이스.

## 참조 파일 (구현 시 먼저 볼 곳)

`build/render.py`(write_pwa ~L3344–3400 · tracker 파싱 ~L3057 · 박물관 오버레이 전례 build_paris_museum_booking ~L2731) · `build/pwa_check.py`(EXCLUDED L41·목록 대조 L105+) · `build/assets/app.js`(L873–1087 오버레이 패턴·L324 today 패널) · `build/site.py` · `.github/workflows/pages.yml` · `data/daily-cards/schema.json`(존재 확인됨 — 클라이언트·서버 공용 스키마로 재사용).
