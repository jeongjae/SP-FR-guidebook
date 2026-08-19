# Place Dedup Migration Map: Luberon (PC-10)

## 1. 개요 (Overview)
- **목적**: `source/CURRENT/20_Regional_Chapters/08_Luberon_Farmhouse_v2.0.md`의 장문 서술을 Canonical Source of Truth (`source/CURRENT/30_Places/<slug>.md`)로 완전 이전하고, 챕터 본문은 Compact Reference / Editor's Verdict / [상세 가이드 보기] 링크 구조로 전환.
- **원칙**: 0 Content Loss (정보 유실 제로), 5-Layer 표준화, 마을별 차별화, Trip Layer 분리.

---

## 2. 장소별 이전 매핑 테이블 (Migration Mapping Table)

| Place Slug | Place Name | Prior Tier / Priority | 30_Places Canonical Path | 이전된 핵심 내용 (5-Layer) | 08 챕터 전환 상태 |
|---|---|---|---|---|---|
| `lourmarin` | Lourmarin | TIER_A / MUST_SEE | `source/CURRENT/30_Places/lourmarin.md` | 알베르 카뮈 영면지(로즈마리 무덤), 앙리 보스코, 프로방스 최초 르네상스 성, 카페 드 로르모, 금요 시장 | Compact Card + 링크 완료 |
| `gordes` | Gordes | TIER_A / MUST_SEE | `source/CURRENT/30_Places/gordes.md` | D15 도로 진입로 파노라마 전망대(Town View Point), 1031년 중세 성채, 지하 도시, 화요 시장(08:30 전 도착 필수) | Compact Card + 링크 완료 |
| `roussillon-sentier-des-ocres` | Roussillon · Sentier des Ocres | TIER_A / MUST_SEE | `source/CURRENT/30_Places/roussillon-sentier-des-ocres.md` | 17가지 황토(Ochre) 지질학, 오커 트레일 50분 산책로, 카스텔뤼스 벨베데레, 복장 수칙(흰옷 금지), 목요 시장 | Compact Card + 링크 완료 |
| `abbaye-de-senanque` | Abbaye Notre-Dame de Sénanque | TIER_A / MUST_SEE | `source/CURRENT/30_Places/abbaye-de-senanque.md` | 1148년 시토회 12세기 로마네스크 수도원, 장식의 배제(절대 청빈), 히스토패드 관람, 침묵/복장 규정, D177 좁은 도로 | Compact Card + 링크 완료 |
| `coustellet` | Marché Paysan de Coustellet | UTILITY / MUST_SEE | `source/CURRENT/30_Places/coustellet.md` | 100% 농가 직거래 정통 생산자 일요 시장(Marché Paysan), 제철 과일/채소, 염소치즈, 농가 체류 식료품 보급선 | Compact Card + 링크 완료 |
| `goult` | Goult | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/goult.md` | 관광버스가 없는 '숨겨진 보석' 생활 마을, 17세기 예루살렘 풍차 전망대, Café de la Poste 사랑방 | Compact Card + 링크 완료 |
| `bonnieux` | Bonnieux | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/bonnieux.md` | 뤼베롱 최대 낙차 계단식 언덕 마을, 정상 Vieille Église 테라스에서 맞은편 라코스트(사드 후작 성) 조망, 금요 시장 | Compact Card + 링크 완료 |
| `village-des-bories` | Village des Bories | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/village-des-bories.md` | 회반죽 없는 건식 석조(Dry-stone) 내어쌓기 20여 채 원추형 오두막 군락, 18~19세기 농민 생활사, 1차선 좁은 진입로 | Compact Card + 링크 완료 |
| `menerbes` | Ménerbes | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/menerbes.md` | 피터 메일 소설 배경지, 피카소 연인 도라 마르 저택, 1km 좁은 능선(Ridge) 위 성채, 와인&트러플 하우스, 목요 시장 | Compact Card + 링크 완료 |
| `oppede-le-vieux` | Oppède-le-Vieux | TIER_C / OPTIONAL | `source/CURRENT/30_Places/oppede-le-vieux.md` | 19세기 버려진 중세 유령 요새 마을, 숲과 덩굴 속 성채 폐허, 복원된 노트르담 달리동 성당, 숲길 15분 하이킹 | Compact Card + 링크 완료 |
| `l-isle-sur-la-sorgue` | L’Isle-sur-la-Sorgue | TIER_B / WORTHWHILE | `source/CURRENT/30_Places/l-isle-sur-la-sorgue.md` | 소르그 강 에메랄드 수로, 15개 목조 물레바퀴, 유럽 3대 앤틱 골동품 도시, 르네 샤르 고향, 일요 대형 시장 | Compact Card + 링크 완료 (**신규 생성**) |

---

## 3. 검증 결과
- **장문 중복 검사**: PASS (시그니처 구문 중복 0건)
- **정보 보존율**: 100% (모든 역사, 건축학적 디테일, 관람 팁, 주의사항이 Canonical SOT에 보존 및 확장됨)
