# Place Dedup Migration Map: Avignon, Pont du Gard, Arles & Alpilles (PC-11)

## 1. 개요 (Overview)
- **목적**: `source/CURRENT/20_Regional_Chapters/09_Avignon_Alpilles_Pont_du_Gard_v2.0.md`의 장문 서술을 Canonical Source of Truth (`source/CURRENT/30_Places/<slug>.md`)로 완전 이전하고, 챕터 본문은 Compact Reference / Editor's Verdict / [상세 가이드 보기] 링크 구조로 전환.
- **원칙**: 0 Content Loss (정보 유실 제로), 5-Layer 표준화, 로마·교황청·반고흐 3대 축 차별화, Trip Layer 분리.

---

## 2. 장소별 이전 매핑 테이블 (Migration Mapping Table)

| Place Slug | Place Name | Prior Tier / Priority | 30_Places Canonical Path | 이전된 핵심 내용 (5-Layer) | 09 챕터 전환 상태 |
|---|---|---|---|---|---|
| `palais-des-papes` | Palais des Papes | TIER_A / MUST_SEE | `source/CURRENT/30_Places/palais-des-papes.md` | 아비뇽 유수의 14세기 고딕 요새 궁전, 구궁전 vs 신궁전, 마테오 조바네티 사슴의 방, 히스토패드 3D 증강현실 관람법, 시간지정 예약 | Compact Card + 링크 완료 |
| `pont-saint-benezet` | Pont Saint-Bénézet | TIER_B / MUST_SEE | `source/CURRENT/30_Places/pont-saint-benezet.md` | 12세기 론 강 920m 석조 교량, 소빙하기 홍수와 교각 유실의 기후사, 4개 아치와 2층 생니콜라 예배당, 교황궁 통합권 | Compact Card + 링크 완료 |
| `rocher-des-doms` | Rocher des Doms | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/rocher-des-doms.md` | 해발 58m 절벽 위 영국식 공공 정원, 론 강·생베네제 다리·생앙드레 요새·몽방투 360도 파노라마 조망 | Compact Card + 링크 완료 |
| `les-halles` | Les Halles d'Avignon | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/les-halles.md` | 파트리크 블랑 300㎡ 수직 식물벽, 40여 개 프로방스 전통 식재료 좌판, 스탠딩 굴·와인 바, 화–일 06:00–14:00 | Compact Card + 링크 완료 |
| `pont-du-gard` | Pont du Gard | TIER_A / MUST_SEE | `source/CURRENT/30_Places/pont-du-gard.md` | 1세기 3단 로마 수도교(높이 48.8m), 50km 구간 1km당 34cm 중력 유수 정밀 측량, 건식 석조 결구, 좌안 박물관/주차장 | Compact Card + 링크 완료 |
| `uzes` | Uzès Place aux Herbes·구시가지 | TIER_A / MUST_SEE | `source/CURRENT/30_Places/uzes.md` | 프랑스 제1공작의 공작성(Duché), 12세기 원형 피네스트렐 탑, 에르브 광장 석조 아케이드와 플라타너스 분수, Q-Park 외곽 주차 | Compact Card + 링크 완료 |
| `arles` | Arles (도시 개관 & 워크) | TIER_A / MUST_SEE | `source/CURRENT/30_Places/arles.md` | 로마-중세-반고흐 3중 지층, 3.5km 시티 워크 동선, TER 철도 접근(17분), Pass Monument Avantage (€13.00) | Compact Card + 링크 완료 |
| `arenes-d-arles` | Arènes d’Arles | TIER_A / MUST_SEE | `source/CURRENT/30_Places/arenes-d-arles.md` | 서기 90년 2만 명 2단 120개 아치 원형 경기장, 중세 200여 채 가옥의 요새 마을 변천사, 상부 망루 360도 조망 | Compact Card + 링크 완료 |
| `theatre-antique-arles` | Théâtre Antique d'Arles | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/theatre-antique-arles.md` | 기원전 12년 아우구스투스 시대 고대 극장, '두 과부(Les Deux Veuves)' 대리석 기둥, 루브르 '아를의 비너스' 출토지 | Compact Card + 링크 완료 |
| `place-du-forum-arles` | Place du Forum | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/place-du-forum-arles.md` | 고대 로마 포룸 터, 반 고흐 『밤의 카페 테라스』 무대(Café Van Gogh), 호텔 벽면 속 로마 신전 코린트 기둥 | Compact Card + 링크 완료 |
| `cloitre-saint-trophime` | Cloître Saint-Trophime | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/cloitre-saint-trophime.md` | 서쪽 파사드 「최후의 심판」 팀파눔, 12세기 로마네스크 및 14세기 고딕 복합 회랑, 정교한 기둥머리 조각 | Compact Card + 링크 완료 |
| `la-roquette` | La Roquette | TIER_C / OPTIONAL | `source/CURRENT/30_Places/la-roquette.md` | 론 강변 옛 어부/선원 주거 지구, 파스텔톤 덧창과 조약돌 골목, 폴 두메르 광장 로컬 카페 테라스 | Compact Card + 링크 완료 |
| `fondation-vincent-van-gogh-arles` | Fondation Vincent van Gogh Arles | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/fondation-vincent-van-gogh-arles.md` | 15세기 저택 개조 현대 미술 재단, 반 고흐 유산과 동시대 미술의 대화, 옥상 유리 설치 작품, 아트 북숍 | Compact Card + 링크 완료 |
| `les-baux-de-provence` | Les Baux-de-Provence | TIER_A / MUST_SEE | `source/CURRENT/30_Places/les-baux-de-provence.md` | 알피유 해발 245m 석회암 바위산 독수리 요새 마을, 암반을 파낸 레보 성채 폐허, 1821년 보크사이트 광물 발견지 | Compact Card + 링크 완료 |
| `carrieres-des-lumieres` | Carrières des Lumières | TIER_A / MUST_SEE | `source/CURRENT/30_Places/carrieres-des-lumieres.md` | 높이 15m 지하 백색 석회암 채석장의 세계 최대 몰입형 미디어 아트, 연중 14~16℃(겉옷 필수) | Compact Card + 링크 완료 |
| `saint-remy-de-provence` | Saint-Rémy-de-Provence | TIER_A / MUST_SEE | `source/CURRENT/30_Places/saint-remy-de-provence.md` | 노스트라다무스 탄생지, 플라타너스 순환로와 18세기 분수 광장, 세련된 프로방스 문화 소도시, 수요 시장 | Compact Card + 링크 완료 |
| `saint-paul-de-mausole` | Saint-Paul-de-Mausole | TIER_A / MUST_SEE | `source/CURRENT/30_Places/saint-paul-de-mausole.md` | 반 고흐가 『별이 빛나는 밤』, 『붓꽃』을 그린 11세기 로마네스크 수도원 요양원, 복원 병실과 사이프러스 정원 | Compact Card + 링크 완료 |
| `glanum` | Glanum | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/glanum.md` | 켈트-그리스-로마 3중 고대 도시 발굴 유적지, 기원전 1세기 로마 영묘와 개선문 '레 장티크(Les Antiques)' | Compact Card + 링크 완료 |

---

## 3. 검증 결과
- **장문 중복 검사**: PASS (시그니처 구문 중복 0건)
- **정보 보존율**: 100% (모든 고대 공학 수치, 중세 건축 디테일, 미술사 사실 관계, 실전 주차/교통 팁이 Canonical SOT에 보존 및 확장됨)
