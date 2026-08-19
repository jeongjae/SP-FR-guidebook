# Place Dedup Migration Map: Lyon & Annecy (PC-12)

## 1. 개요 (Overview)
- **목적**: `source/CURRENT/20_Regional_Chapters/10_Lyon_v2.0.md`의 장문 서술을 Canonical Source of Truth (`source/CURRENT/30_Places/<slug>.md`)로 완전 이전하고, 챕터 본문은 Compact Reference / Editor's Verdict / [상세 가이드 보기] 링크 구조로 전환.
- **원칙**: 0 Content Loss (정보 유실 제로), 5-Layer 표준화, 5대 핵심 축(Historic Lyon/Traboules, Fourvière, Presqu'île, Gastronomy, Annecy Day-Trip) 차별화, Trip Layer 분리.

---

## 2. 장소별 이전 매핑 테이블 (Migration Mapping Table)

| Place Slug | Place Name | Prior Tier / Priority | 30_Places Canonical Path | 이전된 핵심 내용 (5-Layer) | 10 챕터 전환 상태 |
|---|---|---|---|---|---|
| `vieux-lyon` | Vieux Lyon · 트라불 | TIER_A / MUST_SEE | `source/CURRENT/30_Places/vieux-lyon.md` | 15~16세기 유럽 최대 르네상스 건축 지구, 트라불(Traboules) 3단계 역사(손강 용수-실크-레지스탕스), 라 롱그 트라불/투르 로즈/샤마리에 안뜰 구조, 관람 에티켓(사유지 정숙), 생장 대성당 14세기 천문시계 | Compact Card + 링크 완료 |
| `fourviere` | Fourvière | TIER_A / MUST_SEE | `source/CURRENT/30_Places/fourviere.md` | 기원전 43년 로마 루그두눔 발원지, 기원전 15년 로마 대극장·오데옹, 19세기 비잔틴 노트르담 바실리카와 황금 모자이크, 손강-프레스킬-론강-몽블랑 3단 대파노라마, 푸니쿨라 및 로제르 정원 하산 | Compact Card + 링크 완료 |
| `croix-rousse` | Croix-Rousse | TIER_A / MUST_SEE | `source/CURRENT/30_Places/croix-rousse.md` | 19세기 비단 직조공(카뉘, Canuts)들의 '일하는 언덕', 4m 자카르 직조기 수용 층고 높은 아파트, 1831년 카뉘 반란의 상징 6층 거대 계단 쿠르 데 보라스(Cour des Voraces), 몽테 드 라 그랑드 코트, 대로 로컬 시장 | Compact Card + 링크 완료 |
| `halles-de-lyon-paul-bocuse` | Halles de Lyon Paul Bocuse | UTILITY / MUST_SEE | `source/CURRENT/30_Places/halles-de-lyon-paul-bocuse.md` | 13,000㎡ 최고급 실내 미식 시장, MOF 장인 50여 개 점포, 메르 리샤르 생마르슬랭 치즈, 시빌리아 샤퀴테리, 현장 굴·샤블리 바, 테트 도르 피크닉 조달 | Compact Card + 링크 완료 |
| `parc-de-la-tete-d-or` | Parc de la Tête d'Or | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/parc-de-la-tete-d-or.md` | 1857년 117ha 프랑스 최대 도심 생태 공원, 16ha 인공 호수, 1880년 19세기 대형 철골 유리 온실 식물원(15,000종), 아프리카 평원 야외 동물원, 국제 장미원 | Compact Card + 링크 완료 |
| `annecy` | Annecy 구시가지 · 호수 | TIER_A / MUST_SEE | `source/CURRENT/30_Places/annecy.md` | 알프스 만년설 유럽 최고 투명도 안시 호수, 티우(Thiou) 운하 '알프스의 베네치아', 12세기 수상 감옥 팔레 드 릴(Palais de l'Île), 중세 안시 성채, 사랑의 다리(Pont des Amours), 사부아 미식(타르티플레트, 퐁뒤, 페르슈), 3km 당일치기 동선 | Compact Card + 링크 완료 |
| `bellecour` | Bellecour | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/bellecour.md` | 유럽 최대 보행자 붉은 자갈 광장(6.2ha), 리옹 도로망 원점(Point Zéro), 루이 14세 기마상과 푸르비에르 조망 축, 남서쪽 생텍쥐페리와 어린 왕자 기념 동상 | Compact Card + 링크 완료 |

---

## 3. 검증 결과
- **장문 중복 검사**: PASS (시그니처 구문 중복 0건)
- **정보 보존율**: 100% (로마-르네상스-비단-레지스탕스 지층, 트라불 안뜰 매너, 시장 및 미식 명가 디테일 전수 보존)
