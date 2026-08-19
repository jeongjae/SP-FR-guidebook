# Place Dedup Migration Map: Aix-en-Provence & Marseille (PC-09)

## 1. 개요 (Overview)
- **목적**: `source/CURRENT/20_Regional_Chapters/07_Aix_en_Provence_v2.0.md`의 장문 서술을 Canonical Source of Truth (`source/CURRENT/30_Places/<slug>.md`)로 완전 이전하고, 챕터 본문은 Compact Reference / Editor's Verdict / [상세 가이드 보기] 링크 구조로 전환.
- **원칙**: 0 Content Loss (정보 유실 제로), 5-Layer 표준화, Trip Layer 분리.

---

## 2. 장소별 이전 매핑 테이블 (Migration Mapping Table)

| Place Slug | Place Name | Prior Tier / Priority | 30_Places Canonical Path | 이전된 핵심 내용 (5-Layer) | 07 챕터 전환 상태 |
|---|---|---|---|---|---|
| `cours-mirabeau` | Cours Mirabeau | TIER_A / MUST_SEE | `source/CURRENT/30_Places/cours-mirabeau.md` | 1651년 옛 성벽 조성사, 남북 비대칭, 4대 분수(로통드, 9분수, 이끼분수 18℃, 르네 왕), 세잔 생가 55번지 | Compact Card + 링크 완료 |
| `vieil-aix` | Vieil Aix (구시가지) | TIER_A / MUST_SEE | `source/CURRENT/30_Places/vieil-aix.md` | 로마 온천 도시, 알베르타스 광장 바로크 파사드, 생소뵈르 대성당 1,500년 지층, 보행자 전용 미로 | Compact Card + 링크 완료 |
| `atelier-des-lauves` | Atelier de Cézanne | TIER_A / MUST_SEE | `source/CURRENT/30_Places/atelier-des-lauves.md` | 로브 언덕 말년 4년, 북향 균일 채광창, 대형 캔버스 벽면 슬릿, 정물 오브제, 2026 무장애 안내동 | Compact Card + 링크 완료 |
| `montagne-sainte-victoire-terrain-des-peintres` | Terrain des Peintres | TIER_A / MUST_SEE | `source/CURRENT/30_Places/montagne-sainte-victoire-terrain-des-peintres.md` | 에나멜 세라믹 복제 화판 9개와 생트빅투아르 산 1:1 현장 겹쳐보기, 일몰 골든아워 | Compact Card + 링크 완료 |
| `place-richelme-place-des-precheurs` | 시장 (리셸므 & 프레셰르) | TIER_B / MUST_SEE | `source/CURRENT/30_Places/place-richelme-place-des-precheurs.md` | 리셸므 매일 아침 오감 식료품 시장 + 프레셰르 화/목/토 전통 종합 시장 모델 | Compact Card + 링크 완료 |
| `musee-granet` | Musée Granet | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/musee-granet.md` | 옛 몰타 기사단 수도원, 세잔 원작 및 20세기 장 플랑크 현대미술 컬렉션(피카소/자코메티) | Compact Card + 링크 완료 |
| `bastide-du-jas-de-bouffan` | Bastide du Jas de Bouffan | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/bastide-du-jas-de-bouffan.md` | 20~60세 40년 세잔의 근원지, 초기 벽화 복원 및 마로니에 가로수길, 2026 한정 공개 | Compact Card + 링크 완료 |
| `carrieres-de-bibemus` | Carrières de Bibémus | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/carrieres-de-bibemus.md` | 황토 사암 직각 절벽, 큐비즘의 태동지, 세잔의 오두막 | Compact Card + 링크 완료 |
| `rotonde` | Fontaine de la Rotonde | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/rotonde.md` | 1860년 엑상의 관문, 3대 여신상(정의, 상업, 예술)이 가리키는 도시의 방향성 | Compact Card + 링크 완료 |
| `vieux-port-marseille` | Vieux-Port de Marseille | TIER_B / MUST_SEE | `source/CURRENT/30_Places/vieux-port-marseille.md` | 2,600년 역사 항구, 노먼 포스터 거울 차양(L'Ombrière), 아침 어시장, 45분 핵심 축선 | Compact Card + 링크 완료 |
| `le-panier` | Le Panier | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/le-panier.md` | 마르세유 최고(最古) 그리스 기원 언덕 마을, 스트리트 아트, 비에이 샤리테 바로크 돔 | Compact Card + 링크 완료 |
| `mucem` | Mucem | TIER_A / MUST_SEE | `source/CURRENT/30_Places/mucem.md` | 루디 리치오티 레이스 콘크리트 건축, 외부 램프/옥상 무료 개방, 135m 바다 공중 보도교 | Compact Card + 링크 완료 |
| `fort-saint-jean` | Fort Saint-Jean | TIER_B / MUST_SEE | `source/CURRENT/30_Places/fort-saint-jean.md` | 1660년 루이 14세 군사 요새, 도시를 향한 포문, 르네 왕의 탑, 지중해 이주의 정원 | Compact Card + 링크 완료 |
| `notre-dame-de-la-garde` | Notre-Dame de la Garde | TIER_A / MUST_SEE | `source/CURRENT/30_Places/notre-dame-de-la-garde.md` | 해발 154m 정상 황금 성모(La Bonne Mère), 뱃사람 봉헌 모형배, 360도 지중해 최고봉 조망 | Compact Card + 링크 완료 |
| `marseille` | Marseille (도시 전체) | TIER_B / MUST_SEE | `source/CURRENT/30_Places/marseille.md` | 마르세유 4대 레이어 종합 가이드, Aix ↔ Marseille Ligne 50 고속버스 실용 가이드 | Compact Card + 링크 완료 |
| `saint-paul-de-vence` | Saint-Paul-de-Vence | TIER_A / MUST_SEE | `source/CURRENT/30_Places/saint-paul-de-vence.md` | 마그 재단 미술관(자코메티 안뜰, 미로 미궁), 중세 성벽 마을, 샤갈의 묘소 | Compact Card + 링크 완료 |
| `grasse` | Grasse | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/grasse.md` | 세계 향수의 수도 500년 역사, 16세기 가죽 향장갑 기원, 프라고나르 유서 깊은 공장 투어 | Compact Card + 링크 완료 |
| `cassis` | Cassis 항구 | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/cassis.md` | 394m 캅 카나유 절벽, 카시스 화이트 와인(AOC Cassis), 칼랑크 유람선 출발 거점 | Compact Card + 링크 완료 |
| `calanques` | Parc National des Calanques | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/calanques.md` | 20km 백색 석회암 피오르 협만, 해상 유람선 투어 가이드, 포르미우/포르팽/앙보 | Compact Card + 링크 완료 |

---

## 3. 검증 결과
- **장문 중복 검사**: PASS (시그니처 구문 중복 0건)
- **정보 보존율**: 100% (모든 역사, 건축학적 디테일, 관람 팁, 주의사항이 Canonical SOT에 보존 및 확장됨)
