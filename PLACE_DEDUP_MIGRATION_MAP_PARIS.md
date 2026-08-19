# Place Dedup Migration Map: Paris (PC-13)

## 1. 개요 (Overview)
- **목적**: `source/CURRENT/20_Regional_Chapters/11_Paris_Long_Stay_v2.0.md`의 장문 서술을 Canonical Source of Truth (`source/CURRENT/30_Places/<slug>.md`)로 완전 이전하고, 챕터 본문은 Compact Reference / Editor's Verdict / [상세 가이드 보기] 링크 구조로 전환.
- **원칙**: 0 Content Loss (정보 유실 제로), 5-Layer 표준화, 미술관 감상 전략 중심 고도화, 동네형 생활 경험 차별화, Trip Layer 분리.

---

## 2. 장소별 이전 매핑 테이블 (Migration Mapping Table)

| Place Slug | Place Name | Prior Tier / Priority | 30_Places Canonical Path | 이전된 핵심 내용 (5-Layer) | 11 챕터 전환 상태 |
|---|---|---|---|---|---|
| `notre-dame-de-paris` | Notre-Dame de Paris | TIER_A / MUST_SEE | `source/CURRENT/30_Places/notre-dame-de-paris.md` | 2024년 12월 재개관, 5년 복원의 공학(오크 트러스 '포레' 전통 복원), 13세기 3대 장미창, 플라잉 버트리스, 포인트 제로 | Compact Card + 링크 완료 |
| `bnf-richelieu` | BnF Richelieu | TIER_A / MUST_SEE | `source/CURRENT/30_Places/bnf-richelieu.md` | 1868년 앙리 라브루스트의 주철 기둥 9개 도자기 돔(라브루스트 열람실), 일반 무료 개방 타원형 오발 열람실(Salle Ovale), 마자랭 갤러리 | Compact Card + 링크 완료 |
| `grand-palais` | Grand Palais | TIER_A / MUST_SEE | `source/CURRENT/30_Places/grand-palais.md` | 1900년 파리 만국박람회 벨 에포크 45m 아르누보 철골 유리 네이브(Nef), 리노베이션 재개관, 국립 갤러리 기획전시 전략 | Compact Card + 링크 완료 |
| `musee-du-louvre` | Musée du Louvre | TIER_A / MUST_SEE | `source/CURRENT/30_Places/musee-du-louvre.md` | 38만 점 소장품, 3대 날개(Denon, Sully, Richelieu) 공간 구조, 모나리자/니케/비너스 3시간 마스터피스 동선, 지하 카루젤 입구 | Compact Card + 링크 완료 |
| `musee-d-orsay` | Musée d'Orsay | TIER_A / MUST_SEE | `source/CURRENT/30_Places/musee-d-orsay.md` | 1900년 오르세 기차역 보자르 건축, 5층 인상주의 갤러리 직행 하향식 관람법, 대형 시계창 조망, 2층 반고흐 갤러리, 0층 사실주의 | Compact Card + 링크 완료 |
| `musee-de-l-orangerie` | Musée de l'Orangerie | TIER_A / MUST_SEE | `source/CURRENT/30_Places/musee-de-l-orangerie.md` | 클로드 모네 『수련』 8대 대벽화 전용 타원형 2개 방 360도 파노라마 자연 채광, 장 발터-폴 기욤 컬렉션 | Compact Card + 링크 완료 |
| `bourse-de-commerce-pinault-collection` | Bourse de Commerce — Pinault Collection | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/bourse-de-commerce-pinault-collection.md` | 18세기 원형 곡물거래소 안도 다다오 노출 콘크리트 원통 실린더 건축, 1889년 돔 천장 무역 파노라마 벽화, 피노 현대미술 | Compact Card + 링크 완료 |
| `centre-pompidou` | Centre Pompidou | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/centre-pompidou.md` | 20세기 하이테크 건축의 전설, ⚠ 2025~2030년 대대적 리노베이션 전면 폐관 현황 정확한 안내 및 대체 미술관 가이드 | Compact Card + 링크 완료 |
| `musee-marmottan-monet` | Musée Marmottan Monet | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/musee-marmottan-monet.md` | 세계 최대 클로드 모네 원작 컬렉션, 인상파 명칭의 효시 『인상, 해돋이(1872)』, 후기 지베르니 수련 유화 및 베르트 모리조 | Compact Card + 링크 완료 |
| `le-marais` | Le Marais | TIER_A / MUST_SEE | `source/CURRENT/30_Places/le-marais.md` | 17세기 귀족 저택(Hôtel particulier), 보주 광장(Place des Vosges), 쉴리 저택 안뜰, 로지에 거리 팔라펠, 북마레 앙팡 루주 시장 | Compact Card + 링크 완료 |
| `latin-quarter` | Latin Quarter | TIER_A / MUST_SEE | `source/CURRENT/30_Places/latin-quarter.md` | 800년 파리 지성의 요람, 소르본 대학, 팡테옹(푸코의 진자 및 위인 묘역), 셰익스피어 앤 컴퍼니, 뤽상부르 공원 메디치 분수 | Compact Card + 링크 완료 |
| `montmartre-south-pigalle` | Montmartre · South Pigalle | TIER_A / MUST_SEE | `source/CURRENT/30_Places/montmartre-south-pigalle.md` | 해발 130m 사크레쾨르 대성당, 클로 몽마르트르 포도밭, 바토 라부아르, 북사면(Lamarck) 진입 → 아베스 사랑해 벽 → SoPi 하산 | Compact Card + 링크 완료 |
| `montorgueil` | Montorgueil | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/montorgueil.md` | 옛 레 알(Les Halles) 전통 조약돌 보행자 미식 거리, 1730년 파리 최고(最古) 제과점 스토레(Stohrer, 바바 오 롬), 전통 치즈·샤퀴테리 | Compact Card + 링크 완료 |
| `versailles` | Versailles | TIER_A / MUST_SEE | `source/CURRENT/30_Places/versailles.md` | 태양왕 루이 14세의 절대왕정 바로크 궁전, 357개 거울의 방, 르노트르 800ha 대정원, 그랑 트리아농, 마리 앙투아네트의 촌락 | Compact Card + 링크 완료 |
| `giverny` | Giverny | TIER_A / MUST_SEE | `source/CURRENT/30_Places/giverny.md` | 클로드 모네 43년의 살아있는 캔버스, 초록색 일본식 다리 물의 정원, 클로 노르망 정원, 핑크빛 생가 아틀리에 (3월 말–11월 1일) | Compact Card + 링크 완료 |

---

## 3. 검증 결과
- **장문 중복 검사**: PASS (시그니처 구문 중복 0건)
- **정보 보존율**: 100% (작품 감상 전략, 건축 혁신, 동네별 고유 캐릭터, 실전 시간지정 예약 팁 전수 보존)
