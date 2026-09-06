#!/usr/bin/env python3
"""MP-04 — Day 카드의 끼니 슬롯에 상호를 넣는다.

점심 6곳은 이미 있던 food 스톱을 상호로 채우고, 저녁 10곳은 '숙소 귀환 &
저녁' 이라고만 적혀 있던 스톱을 실제 식당으로 바꾼다. 그중 세 밤(마레·
몽마르트르·생제르맹)은 현장에서 먹고 돌아오도록 스톱을 하나 더 세운다.

좌표는 그 날의 **핀**이지 업소 주소가 아니다 — build/render.maps_url 이
이름 검색을 좌표보다 먼저 쓰는 이유와 같다. 새 업소의 실측 좌표는 확보하지
못했고, 추정 좌표를 업소 좌표인 척 넣지 않는다. 길찾기는 map-queries.json
의 상호·주소 검색으로 연다.

    python3 scripts/apply_paris_meal_days.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "data" / "daily-cards"


def load(n):
    return json.loads((CARDS / f"day-{n:02d}.json").read_text(encoding="utf-8"))


def save(n, d):
    (CARDS / f"day-{n:02d}.json").write_text(
        json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stop(d, sid):
    for s in d["stops"]:
        if s["id"] == sid:
            return s
    raise KeyError(f"{sid} 없음")


def es(kind, label, detail):
    return {"type": kind, "label": label, "detail": detail}


COORD_NOTE = "좌표 미확보 — 지도 핀은 권역 기준이고 길찾기는 상호·주소 검색으로 연다"


def merge_backup(prev: str | None, added: str) -> str:
    """대안 문구를 Plan B 앞에 붙인다. 두 번 돌려도 같은 결과가 나온다."""
    prev = (prev or "").strip()
    if added in prev:
        return prev
    return added + (f"\n\n{prev}" if prev else "")

# ── 점심 6슬롯 ────────────────────────────────────────────────────────────
LUNCH = {
    31: dict(sid="opera-lunch", ref="au-petit-riche",
             name="Au Petit Riche 9구 벨에포크 점심",
             summary="1854년 개업한 벨에포크 살롱에서 점심. 모로 미술관에서 도보 10~12분, "
                     "식후 Richelieu-Drouot역 8호선으로 마레까지 환승 없이 10~12분",
             menu="Quenelle de brochet 갑각류 소스 €24 · Tartare de bœuf 칼로 다진 €25 · "
                  "Crème brûlée 마다가스카르 바닐라 €12",
             sts=[es("book", "BOOK", "월요일 점심 영업 확인(출처 3건). 12:00 오픈 — "
                                    "이 권역에서 유일하다. +33 1 47 70 68 68 사전 예약"),
                  es("check", "CHECK", "점심 메뉴 €32 vs €29 로 출처가 갈린다. 예약 전화 시 확인")],
             backup="Au Petit Riche 만석 시 Le Pantruche(3 rue Victor Massé, 3코스 €23, "
                    "12:30 오픈이라 실질 60분) 또는 Caillebotte(8 rue Hippolyte Lebas, 점심 €23). "
                    "둘 다 월요일 점심 영업이지만 12:30 오픈이라 13:30 퇴점을 미리 알린다"),
    34: dict(sid="rue-du-bac-lunch", ref="cafe-varenne",
             name="Café Varenne 7구 점심",
             summary="오르세에서 도보 10분, 식후 rue de Varenne를 8분 직진하면 로댕 미술관. "
                     "07:30~23:00 논스톱이라 관람이 밀려도 따뜻한 점심을 놓치지 않는다",
             menu="Confit de canard 수제 감자튀김 · Œufs mayonnaise · Pâté en croûte maison",
             sts=[es("confirmed", "OPEN", "월–토 07:30–23:00 논스톱(출처 4건 일치) · 일요일 휴무. "
                                          "평균 체류 45분이라 75분 슬롯에 여유가 있다"),
                  es("check", "CHECK", "통 영업시간과 별개로 13:00–14:00에 따뜻한 요리 주문이 "
                                       "되는지 전화(+33 1 45 48 62 72) 확인")],
             backup="La Laiterie Sainte Clotilde(64 rue de Bellechasse, 로댕 도보 5분, 고미요 "
                    "12/20 — 점심 마감이 14:00일 수 있어 빠듯하고 예약 필수) 또는 L'Affable"
                    "(10 rue de Saint-Simon, 점심 코스 €26~29 — 2인 3코스가 예산에 들어오는 유일한 곳)"),
    33: dict(sid="champs-elysees-lunch", ref="chez-savy",
             name="Chez Savy 8구 아르데코 비스트로 점심",
             summary="오랑주리에서 도보 약 15~18분. 아브뉘 몽테뉴 한 블록 안쪽 골목이라 대로변 "
                     "관광객 함정을 물리적으로 피하고, 문을 나서면 곧바로 몽테뉴 산책이 시작된다",
             menu="Épaule d'agneau confite façon Savy €32 · Foie de veau aux lardons · "
                  "Tartare de bœuf, pommes paille",
             sts=[es("book", "BOOK", "패션위크 SS27 3일차다. 이 권역 점심 수요가 급증하니 "
                                     "2~3주 전 전화 예약(+33 1 47 23 46 98)"),
                  es("caution", "CAUTION", "9/30 The Row 12:00 · Balmain 13:30 쇼가 몽테뉴·알마 "
                                           "인근이면 이 시간대에 보행 통제가 생긴다. 출발 1주 전 "
                                           "FHCM 최종 캘린더 확인"),
                  es("check", "CHECK", "예산은 앙트레+메인 2코스에 물(carafe d'eau)로 1인 €33~42")],
             backup="Le Bar des Théâtres(44 rue Jean Goujon, 논스톱 영업이라 시간 리스크 최저, "
                    "TheFork 온라인 예약 가능)"),
    32: dict(sid="versailles-lunch", ref="la-flottille",
             name="La Flottille 대운하 점심",
             summary="궁전 본관 출구에서 정원 중앙축(라토나 → 왕의 길 → 아폴로 분수)을 20~25분 "
                     "걸어 대운하 머리에 닿는다. 90분 슬롯이지만 실질 착석은 65분이라 코스가 "
                     "아니라 단품+디저트로 간다",
             menu="Steak au poivre · Escargots de Bourgogne (Label Rouge) · Tarte Tatin",
             sts=[es("book", "BOOK", "420석인데도 성수기 점심은 온라인 만석이 뜬다. Zenchef 또는 "
                                     "TheFork로 12:45~13:00 슬롯 사전 예약"),
                  es("caution", "CAUTION", "미식 목적지가 아니라 위치로 가는 곳이다. 서비스 편차와 "
                                           "미지근한 음식 지적이 반복된다(TripAdvisor 3.3 / TheFork 8.5)"),
                  es("check", "CHECK", "9/29(화)는 Jardins Musicaux 운영일이라 정원이 유료다. "
                                       "Passport 티켓이 있어야 대운하까지 걸어 나갈 수 있다")],
             backup="La Petite Venise(도보 2~3분, 서비스 평가가 더 안정적이나 1인 평균 €46) 또는 "
                    "La Guinguette·테이크아웃 키오스크(예약 불필요, 30~40분에 끝나 남는 시간을 "
                    "대운하 수변 산책에 쓸 수 있다). 트리아농 복귀는 프티 트랭 편도 €5"),
    40: dict(sid="halles-lunch", ref="aux-crus-de-bourgogne",
             name="Aux Crus de Bourgogne 2구 점심",
             summary="부르스 드 코메르스에서 도보 8분. Rue Montorgueil 본거리가 아니라 한 블록 "
                     "안쪽 rue Bachaumont라 함정 구간을 피한다. Étienne Marcel(4호선) 도보 2~3분이라 "
                     "몽마르트르행 4+12호선 동선과 맞는다",
             menu="Pâté en croûte €10 · Steak tartare, pommes allumettes €18 · Baba au rhum €9",
             sts=[es("book", "BOOK", "<Remember Me> 개막일이라 관람 퇴장이 밀릴 수 있다. "
                                     "13:00 예약 필수(+33 1 42 33 48 24)"),
                  es("check", "CHECK", "점심 포뮬이 €28(2025년 리뷰) vs €32(공식)로 갈린다")],
             backup="개막일 혼잡으로 13:00 퇴장이 밀리면 Le Comptoir de la Gastronomie"
                    "(34 rue Montmartre, 도보 5분, 12:00–22:30 논스톱이라 주방 마감이 없다). "
                    "Chez Denise(도보 3분)는 이야기값은 높지만 양이 많고 서비스가 느긋해 75분에 "
                    "위험하고 내장 요리 비중이 크다"),
    41: dict(sid="iena-lunch", ref="les-marches",
             name="Les Marches 16구 점심",
             summary="기메에서 도보 5분, MAM까지 도보 3~4분. 팔레 드 도쿄 옆 계단 골목의 옛 "
                     "트럭 운전사 식당이다. 저녁 고별 만찬이 숯불 고기이므로 점심은 찬 전채와 "
                     "냉 로스트비프로 가볍게 짠다",
             menu="Œufs Mayonnaise €6.50 · Rosbif sauce gribiche €22 · "
                  "Île flottante aux pralines roses €10",
             sts=[es("book", "BOOK", "매일 12:00–14:30 연중무휴(출처 3건 일치). Zenchef 온라인 "
                                     "또는 +33 1 47 23 52 80 — 12:00 예약이면 13:15까지 여유가 있다"),
                  es("check", "CHECK", "점심 정식가가 €18/€20로 갈리고, 확보한 카르트가 여름판이라 "
                                       "10월 가을 메뉴에서는 가격이 바뀔 수 있다")],
             backup="Hanok, par Misso(기메 박물관 내부, 도보 0분 — 옛 Le Salon des Porcelaines "
                    "자리가 한식당으로 바뀌었다. 국물 국수 기반이라 저녁 만찬 대비 가장 가볍다) "
                    "또는 Monsieur Bleu(팔레 드 도쿄, 전채 2개+카페 구르망 공유로 1인 €25.50)"),
}

# ── 15구·현장 저녁 ────────────────────────────────────────────────────────
DINNER = {
    27: dict(ref="le-relais-du-15eme", name="Le Relais du 15ème 도착 첫 저녁",
             summary="장보기를 마치고 숙소에서 도보 3분. 매일 11:00–22:30 논스톱에 예약이 "
                     "필요 없어, 이동으로 지친 도착일에 판단할 것이 없는 집이다",
             menu="Pizza Margherita · Tagliatelle carbonara · Tiramisu",
             sts=[es("confirmed", "OPEN", "매일 11:00–22:30 논스톱 · 연중무휴 · 예약 불필요"),
                  es("optional", "OPTIONAL", "장보기가 넉넉했다면 숙소식으로 대체해도 된다")],
             food=["첫 장보기 — 필수품만", "Le Relais du 15ème 동네 저녁 (도보 3분·무예약)"]),
    31: dict(ref="guylas", name="Guylas 페르시아 저녁 (15구)",
             summary="마레에서 8호선으로 15구 귀환 후 숙소 도보 4분. 월요일에 확실히 여는 "
                     "몇 안 되는 집이고, 프렌치가 이어진 뒤 장르를 갈아타는 자리다",
             menu="Fesenjan 호두·석류 소스 닭 €18 · Ghalieh 허브·타마린드 스튜 €17 · "
                  "Kebab koobideh 숯불 꼬치",
             sts=[es("confirmed", "OPEN", "연중무휴 매일 영업(출처 3건). 9/28은 월요일이라 "
                                          "15구 프렌치 상당수가 닫는다"),
                  es("check", "CHECK", "마감이 23:30인지 02:00인지 출처가 갈린다. 늦게 갈 때만 확인")],
             food=["숙소 점심", "Guylas 페르시아 저녁 (도보 4분·월요일 영업)"]),
    33: dict(ref="stephane-martin", name="Stéphane Martin 15구 미식 비스트로 저녁",
             summary="숙소에서 도보 4분. Menu du Marché €32면 전채·메인·디저트가 다 들어온다. "
                     "조용한 평일 저녁에 15구의 제대로 된 한 끼를 넣는 자리다",
             menu="Émincé de foie gras de canard cru €19 · Loup de mer, pommes rattes €22 · "
                  "Moelleux au chocolat de Tanzanie €11",
             sts=[es("book", "BOOK", "예약 필수. 공식 홈페이지 또는 TheFork"),
                  es("caution", "CAUTION", "일요일·월요일 휴무. 9/30(수)은 정상 영업이지만 "
                                           "소규모 비스트로라 연차 휴무를 3~7일 전 확인")],
             food=["가벼운 점심 (11:30)", "Stéphane Martin 저녁 (도보 4분·예약 필수)"]),
    35: dict(ref="sawadee-paris", name="Sawadee 태국 저녁 (15구)",
             summary="루브르 4시간 관람과 센 강변 일몰 산책 뒤 숙소 도보 4분. 프렌치가 "
                     "일주일 넘게 이어진 시점에 얼큰한 국물을 넣는다",
             menu="Soupe de crevettes à la citronnelle 똠얌 €8 · 바나나잎 코코넛 대구 €16 · "
                  "Mangue fraîche au riz gluant €12",
             sts=[es("book", "BOOK", "전화 예약만 받는다 — +33 1 45 77 68 90"),
                  es("check", "CHECK", "일요일·월요일 영업이 출처마다 정반대다. 10/2은 금요일이라 "
                                       "문제없지만 날짜를 옮길 때는 전화로 확인")],
             food=["시장식 또는 숙소 점심", "Sawadee 태국 저녁 (도보 4분·전화 예약)"]),
    36: dict(ref="le-relais-du-15eme", name="Le Relais du 15ème 조기 저녁",
             summary="익일 개선문상 경마를 위해 일찍 쉬는 날이다. 논스톱 영업이라 18시에 먹고 "
                     "19:30에 들어올 수 있고 예약도 필요 없다",
             menu="Pizza Margherita · Penne arrabbiata · Tiramisu",
             sts=[es("confirmed", "OPEN", "매일 11:00–22:30 논스톱 · 예약 불필요"),
                  es("optional", "OPTIONAL", "조기 취침이 우선이면 숙소식으로 대체한다")],
             food=["점심·휴식 12:30–14:00", "Le Relais du 15ème 조기 저녁 (18시·도보 3분)"]),
    37: dict(ref="breizh-cafe-charles-michels", name="Breizh Café 갈레트 저녁 (15구)",
             summary="롱샹에서 지쳐 돌아오는 날이다. 일요일 11:30–22:00 연속이라 도착 시간이 "
                     "자유롭고, 갈레트 한 장이면 40분에 끝난다. 숙소 도보 5분",
             menu="Galette andouille de Guémené €17.00 · Huîtres Prat-ar-Coum 6개 €18.50 · "
                  "Crêpe caramel au beurre salé €7.80",
             sts=[es("confirmed", "OPEN", "금·토·일 11:30–22:00 브레이크 없음 · 연중무휴. "
                                          "10/4은 일요일이라 도착 시간을 맞출 필요가 없다"),
                  es("optional", "OPTIONAL", "굴과 농가 시드르를 붙이면 가벼운 저녁이 특별해진다")],
             food=["경기장 식사", "Breizh Café 갈레트 저녁 (도보 5분·일요일 연속영업)"]),
    38: dict(ref="le-volant-basque", name="Le Volant Basque 바스크 저녁 (15구)",
             summary="자크마르-앙드레와 몽소 공원 뒤 15구 귀환. 월요일 저녁에 문을 여는 몇 "
                     "안 되는 정통 프렌치이고, 18:45에 열어 피곤한 날에도 이르게 먹을 수 있다",
             menu="Axoa de veau au piment d'Espelette · Pâté basque au piment doux · "
                  "Trou normand €12",
             sts=[es("book", "BOOK", "월요일은 저녁만 18:45–22:45 영업(공식 2개 페이지 일치) · "
                                     "일요일 휴무. 월요일은 특히 예약 권장 — +33 1 45 75 27 67"),
                  es("check", "CHECK", "개별 요리 가격은 카테고리 범위(전채 €9~16 · 메인 €23~32)만 "
                                       "공개돼 있다")],
             food=["브런치·숙소 점심", "Le Volant Basque 저녁 (도보 7~8분·월요일 영업)"]),
}

# ── 현장 저녁 3밤 (스톱을 하나 더 세운다) ────────────────────────────────
FIELD = {
    29: dict(ref="bouillon-racine", sid="bouillon-racine-dinner",
             after="notre-dame-compact", anchor="saint-germain",
             start="19:00", end="20:30",
             name="Bouillon Racine 저녁 (6구 아르누보)",
             summary="노트르담·시테섬에서 생미셸 대로를 따라 도보 12분. 1906년 개업한 프랑스 "
                     "역사기념물 실내라 저녁 식사 자체가 그날 산책의 마무리가 된다",
             menu="6 escargots de Bourgogne €11 · Jarret de veau façon osso buco · "
                  "Tartare de bar au citron vert €11",
             sts=[es("book", "BOOK", "토요일 저녁이다. 2주 전 bouillonracine.fr 온라인 예약. "
                                     "2층 대형 홀이라 소규모 비스트로보다는 잡히는 편이다"),
                  es("check", "CHECK", "저녁 서비스가 19:00 시작인지 12:00–23:00 연속인지 "
                                       "출처가 갈린다. 예약 시 확인")],
             leg_in=dict(mode="walk", duration="12분", distance="0.9km"),
             leg_out=dict(mode="metro", duration="메트로 10+8호선 약 30분", distance="6.5km"),
             ret_start="20:45", ret_end="21:15",
             ret_name="15구 숙소 귀환", ret_summary="Cluny-La Sorbonne 10호선 → "
             "La Motte-Picquet-Grenelle 8호선 환승 → Lourmel",
             food=["가벼운 점심 — 긴 대기 회피", "Bouillon Racine 저녁 (6구·2주 전 예약)"],
             backup="예약이 안 잡히면 L'Avant Comptoir(3 carrefour de l'Odéon, 매일 11:00–23:00 "
                    "연속, 예약 자체가 없어 시간에 쫓기지 않는다). 다만 좌석이 없고 전원 서서 먹는다"),
    39: dict(ref="chez-janou", sid="chez-janou-dinner",
             after="musee-carnavalet", anchor="musee-carnavalet",
             start="19:00", end="20:30",
             name="Chez Janou 저녁 (마레 프로방스)",
             summary="보주 광장에서 도보 4분. 30년 넘은 동네 프로방스 식당이라 rue des Rosiers "
                     "관광 축에서 비껴 있다. Chemin Vert에서 8호선을 타면 환승 없이 15구까지 직행",
             menu="Ratatouille froide · Petits farcis provençaux · Mousse au chocolat "
                  "(도기 볼째 무제한)",
             sts=[es("book", "BOOK", "1~2주 전 예약(chezjanou.com 또는 +33 1 42 72 28 41). "
                                     "예약 시간에 늦으면 테이블을 넘긴다"),
                  es("caution", "CAUTION", "저녁 서비스는 19:00에 연다. 카르나발레·보주 광장을 "
                                           "18:45에 끝내고 도보 6분으로 이동한다 — 19:00 예약에 "
                                           "여유가 없다")],
             trim=("musee-carnavalet", "18:45"),
             leg_in=dict(mode="walk", duration="6분", distance="0.5km"),
             leg_out=dict(mode="metro", duration="메트로 8호선 직통 약 35분", distance="7.2km"),
             ret_start="20:45", ret_end="21:15",
             ret_name="15구 숙소 귀환", ret_summary="Chemin Vert 8호선 Balard 방면 직통 → Lourmel "
             "(환승 없음)",
             food=["숙소 점심", "Chez Janou 마레 저녁 (19:00·예약 필수)"],
             backup="Au Bourguignon du Marais(52 rue François Miron, 매일 영업, 고미요 예산 "
                    "€25~30 — 뵈프 부르기뇽과 베르티용 아이스크림 프로피트롤). 귀가는 M1+M8 약 45분"),
    40: dict(ref="le-progres-montmartre", sid="le-progres-dinner",
             after="vendanges-montmartre", anchor="vendanges-montmartre",
             start="17:45", end="19:00",
             name="Le Progrès 몽마르트르 이른 저녁",
             summary="Abbesses 역 앞 아르누보 동네 비스트로. 주방이 12:00–22:30 논스톱이라 "
                     "몽마르트르에서 17:45에 실제로 저녁을 먹을 수 있는 몇 안 되는 집이고, "
                     "Place du Tertre 관광 축에서 벗어난 내리막 골목에 있다",
             menu="Tartare de bœuf, frites maison €16.50 · Filets de daurade royale rôtis €23 · "
                  "Linguine à la ricotta et au citron €17.50",
             sts=[es("book", "BOOK", "매일 주방 12:00–22:30 논스톱 — 몽마르트르의 평판 좋은 "
                                     "비스트로는 대부분 19:00 이후에만 열어 이 시간대에 못 쓴다. "
                                     "17:45는 워크인도 대체로 되지만 축제 개막일이므로 TheFork 예약"),
                  es("check", "CHECK", "Abbesses는 파리에서 가장 깊은 역 중 하나다. 엘리베이터 줄이 "
                                       "길면 도보 6분의 Pigalle역이 실질적으로 더 빠르다")],
             trim=("vendanges-montmartre", "17:30"),
             leg_in=dict(mode="walk", duration="내리막 도보 10~12분", distance="0.8km"),
             leg_out=dict(mode="metro", duration="메트로 12+8호선 약 35분", distance="7.5km"),
             ret_start="19:15", ret_end="20:30",
             ret_name="15구 숙소 귀환", ret_summary="Abbesses 12호선 → Concorde 8호선 환승 → Lourmel",
             food=["축제권 점심", "Le Progrès 몽마르트르 이른 저녁 (17:45·논스톱)"],
             backup="Bouillon Pigalle(22 bd de Clichy, 매일 12:00–24:00 연속, 1인 €22~28, 300석이라 "
                    "축제 인파에도 자리 흡수력이 크다). 17:30~18:00이 대기가 가장 짧은 시간대다"),
}


def apply_lunch():
    for n, c in LUNCH.items():
        d = load(n)
        s = stop(d, c["sid"])
        s["name"] = c["name"]
        s["summary"] = c["summary"]
        s["menu"] = c["menu"]
        s["reservation"] = None
        s["executionStatuses"] = c["sts"] + [es("check", "CHECK", COORD_NOTE)]
        s["place_ref"] = c["ref"]
        d["backup"] = merge_backup(d.get("backup"), c["backup"])
        save(n, d)


def apply_dinner():
    for n, c in DINNER.items():
        d = load(n)
        s = stop(d, "paris-return")
        s["category"] = "food"
        s["name"] = c["name"]
        s["summary"] = c["summary"]
        s["menu"] = c["menu"]
        s["reservation"] = None
        s["executionStatuses"] = c["sts"] + [es("check", "CHECK", COORD_NOTE)]
        s["place_ref"] = c["ref"]
        d["food"] = c["food"]
        save(n, d)


def apply_field():
    for n, c in FIELD.items():
        d = load(n)
        anchor = stop(d, c["anchor"])
        new = {
            "id": c["sid"], "order": 0, "start": c["start"], "end": c["end"],
            "name": c["name"], "category": "food",
            "lat": anchor["lat"], "lng": anchor["lng"],
            "summary": c["summary"], "menu": c["menu"], "reservation": None,
            "executionStatuses": c["sts"] + [es("check", "CHECK", COORD_NOTE)],
            "optional": False, "place_ref": c["ref"],
        }
        # 멱등 — 이미 세워 둔 스톱이 있으면 지우고 다시 넣는다
        stops = [s for s in d["stops"] if s["id"] != c["sid"]]
        d["legs"] = [l for l in d["legs"]
                     if c["sid"] not in (l["from"], l["to"])]
        out = []
        for s in stops:
            out.append(s)
            if s["id"] == c["after"]:
                out.append(new)
        if c.get("trim"):
            stop(d, c["trim"][0])["end"] = c["trim"][1]
        ret = stop(d, "paris-return")
        ret["start"], ret["end"] = c["ret_start"], c["ret_end"]
        ret["name"], ret["summary"] = c["ret_name"], c["ret_summary"]
        ret["category"] = "transport"
        ret["menu"] = None
        ret["executionStatuses"] = []
        for i, s in enumerate(out, 1):
            s["order"] = i
        d["stops"] = out

        # 레그도 멱등하게 다시 세운다 — 원래 있던 "직전 방문지 → 귀가" 한 줄을
        # "직전 방문지 → 식당 → 귀가" 두 줄로 바꾼다.
        legs = [l for l in d["legs"]
                if c["sid"] not in (l["from"], l["to"])
                and not (l["from"] == c["after"] and l["to"] == "paris-return")]
        legs.append({"from": c["after"], "to": c["sid"],
                     "mode": c["leg_in"]["mode"], "duration": c["leg_in"]["duration"],
                     "distance": c["leg_in"]["distance"], "line": None,
                     "geometryStatus": "coordinate-line"})
        legs.append({"from": c["sid"], "to": "paris-return",
                     "mode": c["leg_out"]["mode"], "duration": c["leg_out"]["duration"],
                     "distance": c["leg_out"]["distance"], "line": None,
                     "geometryStatus": "coordinate-line"})
        d["legs"] = legs
        d["food"] = c["food"]
        d["endTime"] = c["ret_end"]
        d["backup"] = merge_backup(d.get("backup"), c["backup"])
        save(n, d)


def fix_vendanges():
    """10/7 은 축제 개막일이지만 노점·행렬은 10/9~11 이다. 문구를 정직하게 고친다."""
    d = load(40)
    s = stop(d, "vendanges-montmartre")
    s["name"] = "몽마르트르 산책 & Clos Montmartre 포도밭 (축제 개막일)"
    s["summary"] = (
        "제93회 Fête des Vendanges는 10/7~10/11이고 10/7은 개막일이다. 다만 이날 "
        "공개 행사는 19:00 18구 구청 개막 파티뿐이고, 미식 노점(Parcours du Goût)은 "
        "10/9~11, 대행렬은 10/10(토)에 열린다. 차량 통제도 10/9부터다. 즉 이날 오후는 "
        "축제 현장이 아니라 평상시 몽마르트르다 — Clos Montmartre 포도밭 외관, 라팽 아질, "
        "사크레쾨르 파리 전경을 여유롭게 걷는 날로 잡는다")
    s["executionStatuses"] = [
        {"type": "caution", "label": "CAUTION",
         "detail": "축제 노점·행렬은 10/9~11 주말이다. 10/7 오후에 축제 현장을 기대하면 어긋난다"},
        {"type": "optional", "label": "OPTIONAL",
         "detail": "Clos Montmartre 포도밭 가이드 투어는 10/7 11:00 사전예약제이나 "
                   "부르스 드 코메르스 관람과 시간이 겹친다"},
    ]
    note = ("Fête des Vendanges 2026 공식 프로그램 재확인 — 10/7 개막일 공개행사는 19:00 구청 "
            "파티뿐이고 노점·행렬은 10/9~11 로 확인(2026-08-25). 축제 체험이 목적이면 날짜 이동 검토")
    keep = [x for x in d.get("needsReview", [])
            if "Vendanges de Montmartre 10/7" not in x and x != note]
    d["needsReview"] = keep + [note]
    save(40, d)


def main() -> int:
    apply_lunch()
    apply_dinner()
    apply_field()
    fix_vendanges()
    print(f"점심 {len(LUNCH)} · 15구 저녁 {len(DINNER)} · 현장 저녁 {len(FIELD)} 반영 · "
          f"Day 40 축제 문구 정정")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
