# 콘텐츠 품질 스코어카드

`python3 build/content_quality.py --write` 가 생성한다. 손으로 고치지 않는다.
기준과 목표치는 `CONTENT_QUALITY_PLAN_v1.0.md` 에 있다.

## 지표

| 축 | 지표 | 현재 |
|---|---|---:|
| C1 | 본문 없는 spot | **13** / 94 |
| C1 | 위키 참고 없는 항목 | 10 |
| C1 | dossier ↔ 레지스트리 이름 불일치 | **22** / 51 |
| C2 | dossier 서술 중앙값 | **41자** (표·목록 포함 전체 242자) |
| C2 | 등급별 분량 하한 미달 | **51** / 51 |
| C3 | 운영정보 줄 | 291 |
| C3 | 근거 표기 | 291 (100%) |
| C3 | **무근거** | **0** |
| C6 | 취소 공연 잔재 | 67 |
| C6 | `후보` 표기 | 70 |
| C6 | pending 미분류 | 21 / 291 |
| 사진 | 필수 등급 커버리지 | 35 / 48 |
| 사진 | 전체 spot 커버리지 | 55 / 94 |

## C4 — dossier 요소 결측

| 요소 | 결측 |
|---|---:|
| why_go | 51 |
| 정체성 | 21 |

## dossier ↔ 레지스트리 이름 불일치

이 제목들은 dossier 로는 존재하지만 레지스트리의 장소와 이어지지 않는다 —
**글은 있는데 그 장소 페이지에서는 보이지 않는다.**

Recinte Modernista de Sant Pau, Gothic Quarter·Plaça del Rei, Cau Ferrat·Maricel, Sitges, Girona Walls, Collioure Château Royal, Chemin du Fauvisme, Pals Medieval Quarter, Colline du Château, Cannes Le Suquet·Croisette, Monaco-Ville, Cassis Harbour, Roussillon·Sentier des Ocres, Les Halles Avignon, Uzès Saturday Market, Fourvière Basilica·Roman Hill, Vieux Lyon·Traboules, Annecy Old Town·Lake, Louvre Museum, Musée d’Orsay, Montmartre·South Pigalle, Giverny Fondation Monet, Bourse de Commerce

## 본문 없는 spot

Sitges, Calella de Palafrugell, Collioure, Girona Cathedral, Onyar 강변, Pals, Peralada, Peratallada, Cannes, Monaco, Rotonde, L’Isle-sur-la-Sorgue, Bellecour

## 필수 등급 사진 없음

Le Rocher — 모나코 구시가지, Marseille, Vieux-Port, Mucem, Fort Saint-Jean, 시장 — Place Richelme · Place des Prêcheurs, Coustellet 생산자 시장, Roussillon · Sentier des Ocres, Les Halles, Arles, Arènes d’Arles, Théâtre antique, Montmartre · South Pigalle

---

**이 표가 판정하지 못하는 것**: 문장의 읽는 맛, 편집 판단의 설득력, 사진의 적절성.
전부 통과해도 품질이 확인된 것이 아니다 — 라운드마다 표본을 읽어서 본다.
