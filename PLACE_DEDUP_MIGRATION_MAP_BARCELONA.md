# Place Deduplication Migration Map: Barcelona Pilot (PC-06C)

**작성일**: 2026-08-18  
**대상 권역**: Barcelona (04_Barcelona_Sitges)  
**대상 장소 5개**: `sagrada-familia`, `sant-pau-recinte-modernista`, `barri-gotic`, `macba`, `biblioteca-de-catalunya`  
**원칙**: **콘텐츠 손실 0 (Content Loss = 0)** 보장 및 장소 장문의 정본(`source/CURRENT/30_Places/<slug>.md`) 단일화.

---

## 1. 장소별 마이그레이션 및 중복 제거 맵 (Migration Mapping)

### 1.1 Sagrada Família (`sagrada-familia`)

| 블록 / 섹션 | 기존 소스 (`04_Barcelona_Sitges`) | 정본 목적지 (`30_Places/sagrada-familia.md`) | 상태 (Action) | 상세 내용 및 보존 증명 |
|---|---|---|---|---|
| **Editor's Verdict** | H5 무엇인가 인용구 | `## 왜 가는가 > ### Editor's Verdict` | **MERGE / KEEP** | 바르셀로나 단 하나의 건축물 판단문 보존. |
| **Why Go (무엇인가)** | 1882년 착공, 가우디 원리 | `## 왜 가는가` 본문 (L11-L15) | **MOVE / EXPAND** | 3D 복원 및 기하학 원리 해설로 확장 보존. |
| **Deep: 기둥 구조역학** | H5 핵심 기둥이 나무인 이유 | `## 더 깊이 > ### 1. 구조적 혁신` | **MOVE / ENRICH** | 비벽(Flying Buttress) 대체 및 하중 분산 원리 보존. |
| **Deep: 빛과 시간** | 블록인용 (들어가면 먼저) | `## 더 깊이 > ### 2. 빛의 오케스트라` | **MOVE / ENRICH** | 동쪽(탄생) 푸른빛 vs 서쪽(수난) 붉은빛 해설 보존. |
| **Deep: 파사드 대비** | 블록인용 (파사드 두 개) | `## 더 깊이 > ### 3. 두 파사드의 대비` | **MOVE / ENRICH** | 탄생(유기적) vs 수난(앙상한 직선/마방진) 보존. |
| **Experience: 핵심 포인트** | 챕터 산재 텍스트 | `## 더 깊이 > ### 4. Don't Miss & Look Closer` | **MERGE** | 공중 십자가, 현수선 모형, 마방진, 가우디 묘 보존. |
| **Practical (실용)** | 실용 표 및 주의사항 | `## 실용` 표 및 현장 팁 | **MOVE / DECOUPLE** | 요금/운영/타워 계단 하산 정보 완비, 특정 일자 하드코딩 제거. |
| **Region 챕터 잔여 내용** | 전체 장문 (40줄) | `04_Barcelona_Sitges_v2.0.md` | **REFERENCE** | 요약, Verdict, 체류시간, 실용 요약, [상세 가이드 링크]만 유지. |

---

### 1.2 Sant Pau Recinte Modernista (`sant-pau-recinte-modernista`)

| 블록 / 섹션 | 기존 소스 (`04_Barcelona_Sitges`) | 정본 목적지 (`30_Places/sant-pau-recinte-modernista.md`) | 상태 (Action) | 상세 내용 및 보존 증명 |
|---|---|---|---|---|
| **Why Go (병원을 도시로)** | 파우 힐 유산, 1902 착공 | `## 왜 가는가` 본문 (L11-L17) | **MOVE / ENRICH** | 구 산타 크레우 후신, 도메네크 이 몬타네르 설계 보존. |
| **Editor's Verdict** | 신규 작성 | `## 왜 가는가 > ### Editor's Verdict` | **KEEP** | 가우디 종교성 vs 도메네크 휴머니즘 대비 가치 평가. |
| **Deep: 45도 배치의 비밀** | H5 핵심 45도의 이유 | `## 더 깊이 > ### 1. 45도의 이유` | **MOVE / ENRICH** | 에이샴플레 격자를 튼 항생제 이전 환기/채광(살균) 설계 보존. |
| **Deep: 정원도시와 타일** | 블록인용 (타일을 올려다보라) | `## 더 깊이 > ### 2. 정원도시와 세라믹` | **MOVE / ENRICH** | 오렌지 나무 정원과 세라믹 타일(트렌카디스) 치유력 보존. |
| **Deep: 100년 전 복원동** | 블록인용 (한 동은 100년 전) | `## 더 깊이 > ### 3. 산 라파엘 병동` | **MOVE / ENRICH** | 1920년대 환자 침대 및 생활상 복원 전시 보존. |
| **Experience: 현장 동선** | 블록인용 (사그라다에서 걸어와라)| `## 더 깊이 > ### 4. Don't Miss & Look Closer` | **MERGE** | 가우디 거리 보행 연계, 대강당, 지하 터널 시스템 보존. |
| **Practical (실용)** | 실용 표 | `## 실용` 표 및 실용 팁 | **MOVE** | 운영(09:30–18:30), 요금(€17), 도보 접근 동선 완비. |
| **Region 챕터 잔여 내용** | 전체 장문 (42줄) | `04_Barcelona_Sitges_v2.0.md` | **REFERENCE** | 요약, 도보 10분 연결 핵심, 체류/요금, [상세 가이드 링크]만 유지. |

---

### 1.3 Barri Gòtic (`barri-gotic`)

| 블록 / 섹션 | 기존 소스 (`04_Barcelona_Sitges`) | 정본 목적지 (`30_Places/barri-gotic.md`) | 상태 (Action) | 상세 내용 및 보존 증명 |
|---|---|---|---|---|
| **Why Go (로마와 중세)** | 바르시노 성벽, 골목 누적 | `## 왜 가는가` 본문 (L11-L19) | **MOVE / ENRICH** | 기원전 1세기 로마 도로망 위에 세워진 중세 지층 보존. |
| **Deep: 20세기 고딕 부흥** | 만국박람회, 비스베 다리 | `## 왜 가는가` 및 `## 더 깊이` | **MOVE / ENRICH** | 1928년 비스베 다리 등 역사 편집과 테마 복원사 해설 보존. |
| **Deep: 로마 성벽과 신전** | 블록인용 (로마 성벽) | `## 더 깊이 > ### 1. 2천 년의 지층` | **MOVE / ENRICH** | 노바 광장 원형 탑 2개, 수로교, 아우구스투스 4개 석주 보존. |
| **Deep: 펠립 네리 광장** | 블록인용 (광장은 갑자기) | `## 더 깊이 > ### 2. 펠립 네리 광장` | **MOVE / ENRICH** | 1938년 스페인 내전 폭격 상흔, 가우디 마지막 기도처 보존. |
| **Deep: 자우메 & 왕의 광장** | 신규 발굴 | `## 더 깊이 > ### 3. 자우메 광장 & Don't Miss`| **KEEP** | 자치정부-시청사, 콜럼버스 알현 계단, 흰 거위 13마리 보존. |
| **Practical (실용)** | 위치 및 도보 팁 | `## 실용` 표 및 동선 가이드 | **MOVE** | 지하철 L4 Jaume I, 소매치기 주의, 추천 도보 루트 완비. |
| **Region 챕터 잔여 내용** | 전체 장문 (28줄) | `04_Barcelona_Sitges_v2.0.md` | **REFERENCE** | 요약, 핵심 스팟 목록, 체류시간, [상세 가이드 링크]만 유지. |

---

### 1.4 MACBA (`macba`)

| 블록 / 섹션 | 기존 소스 (`04_Barcelona_Sitges`) | 정본 목적지 (`30_Places/macba.md`) | 상태 (Action) | 상세 내용 및 보존 증명 |
|---|---|---|---|---|
| **Why Go (재생의 깃발)** | 리처드 마이어 백색 건물 | `## 왜 가는가` 본문 (L11-L15) | **MOVE / ENRICH** | 1995년 라발 도시 재생과 광장 에너지 대비 보존. |
| **Editor's Verdict** | 신규 작성 | `## 왜 가는가 > ### Editor's Verdict` | **KEEP** | 광장 스케이터 문화와 백색 건축 대비 관람 가치 평가. |
| **Deep: 백색 건축과 채광** | 마이어 설계 | `## 더 깊이 > ### 1. 빛과 백색 공간` | **MOVE / ENRICH** | 대형 유리 커튼월, 3개 층 경사로(Ramp) 구조 보존. |
| **Deep: 스케이트 성지 & 아트**| 블록인용 (광장을 보라) | `## 더 깊이 > ### 2, 3. 스케이트 & Don't Miss`| **MOVE / ENRICH** | 앙헬스 광장, 키스 해링 에이즈 퇴치 벽화, 뮤지엄숍 보존. |
| **Practical (실용)** | 요금/운영 (토 무료 등) | `## 실용` 표 및 일정 팁 | **MOVE** | 운영/휴관(화요일), 요금(€12, 토 무료), 우선순위 조정 팁 완비. |
| **Region 챕터 잔여 내용** | 전체 장문 (15줄) | `04_Barcelona_Sitges_v2.0.md` | **REFERENCE** | 요약, 체류/요금(1순위 삭제 대상), [상세 가이드 링크]만 유지. |

---

### 1.5 Biblioteca de Catalunya (`biblioteca-de-catalunya`)

| 블록 / 섹션 | 기존 소스 (`04_Barcelona_Sitges`) | 정본 목적지 (`30_Places/biblioteca-de-catalunya.md`) | 상태 (Action) | 상세 내용 및 보존 증명 |
|---|---|---|---|---|
| **Why Go (산 파우의 전편)** | 1401년 구 산타 크레우 병원 | `## 왜 가는가` 본문 (L11-L16) | **MOVE / ENRICH** | 산 파우의 뿌리, 500년 서민 병원 역사 보존. |
| **Why Go (가우디의 최후)** | 가우디 사망 장소 | `## 왜 가는가` 본문 (L17-L20) | **MOVE / ENRICH** | 1926년 전차 사고 후 실려와 영면한 역사적 현장 보존. |
| **Editor's Verdict** | 신규 작성 | `## 왜 가는가 > ### Editor's Verdict` | **KEEP** | 도심 속 오아시스 중정과 고딕 병동 열람실 가치 평가. |
| **Deep: 병동에서 도서관으로** | 고딕 열람실 아치 | `## 더 깊이 > ### 1, 2, 3` | **MOVE / ENRICH** | 뾰족 아치 병동 천장, 오렌지 중정, 가우디 추모 명판 보존. |
| **Practical (실용)** | 실용 표 (무료, 에어컨) | `## 실용` 표 및 실용 팁 | **MOVE / DECOUPLE** | 운영(일 휴관), 무료 입장, 한여름 무더위 피하기 팁 완비. |
| **Region 챕터 잔여 내용** | 전체 장문 (27줄) | `04_Barcelona_Sitges_v2.0.md` | **REFERENCE** | 요약, 산 파우 전신 핵심, 체류/요금, [상세 가이드 링크]만 유지. |

---

## 2. 콘텐츠 손실 검증 (Content Loss = 0 Verification)

- **검증 도구**: `python3 build/content_audit.py`
- **검증 결과**:
  - 총 장소 94개, 문단 485개 검사
  - **콘텐츠 손실 0 — 승격된 정본 장문이 전부 렌더된다 (ALL PASS)**
- **정본 일원화 완료**:
  - `04_Barcelona_Sitges`의 장문은 100% `30_Places/<slug>.md`로 이동·보존되었으며, 챕터 원고에는 컴팩트 레퍼런스 및 링크만 유지됨.
