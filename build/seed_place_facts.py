#!/usr/bin/env python3
"""S0 T0-1 — data/place-facts.json 시드 적재.

출처는 두 개뿐이다 (웹 조사 금지):
  · docs/diagnosis-v2/SPFR_확정사실원장_v1.0.md      (2026-08-16 공식 소스 검증 완료)
  · docs/diagnosis-v2/SPFR_신규확정사실_v2.0.csv     (2026-08-17 신규 75건)

placeId 는 source/ASSETS/91_Place_Registry_v1.0.md 의 slug 를 그대로 쓴다.
값의 소속(placeId)을 확신할 수 없는 시드 행은 적재하지 않고 UNMAPPED 로 보고한다 —
엉뚱한 장소에 확정값을 붙이는 것이 값을 비워 두는 것보다 위험하다.
"""
import csv
import json
import pathlib
import re
from datetime import date

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIAG = ROOT / "docs/diagnosis-v2"
OUT = ROOT / "data/place-facts.json"
REGISTRY = ROOT / "source/ASSETS/91_Place_Registry_v1.0.md"

LEDGER = "2026-08-16 확정 원장 (공식 소스 검증 완료)"
CSV_SRC = "2026-08-17 신규 검증"
D16, D17 = "2026-08-16", "2026-08-17"

TTL = {"price_adult": 180, "price_range": 180, "hours": 90, "closed": 90,
       "booking": 90, "getting_there": 30, "duration": 365, "note": 90}

GRADE_MAP = {"필수": "essential", "우선 추천": "priority", "선택": "optional",
             "대체": "alternative", "비추천": "excluded", "—": "none", "미정": "none"}


def registry():
    """레지스트리 slug → (region, displayName, grade)"""
    out, region = {}, None
    for line in REGISTRY.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^##\s+([a-z][\w-]*)", line)
        if m:
            region = m.group(1)
        m2 = re.match(r"^\|\s*`([a-z0-9-]+)`\s*\|\s*([^|]+)\|\s*(\w+)\s*\|\s*([^|]*)\|", line)
        if m2 and m2.group(3) == "spot" and region:
            out[m2.group(1)] = (region, m2.group(2).strip(),
                                GRADE_MAP.get(m2.group(4).strip(), "none"))
    return out


def F(value, source, verified_at, confidence="official", key=None, blocked=None):
    rec = {"value": value, "confidence": confidence}
    if source:
        rec["source"] = source
    if verified_at:
        rec["verified_at"] = verified_at
    if key:
        rec["ttl_days"] = TTL.get(key, 90)
    if blocked:
        rec["blocked_reason"] = blocked
    return rec


# ── 시드 ────────────────────────────────────────────────────────────────
# 값은 원장·CSV 원문 그대로. 주석의 (L·n) 은 원장 행 / CSV 행 번호.
SEED = {
    # ===== Avignon 권역 (원장 §3) =====
    "palais-des-papes": dict(
        hours=("3/1–11/1 09:00–19:00", LEDGER, D16),
        price_adult=("€16 (통합권 궁+정원+다리 €19.50, 2026-08-01 인상)", LEDGER, D16),
        booking=("시간지정 예약 의무 아님 (권장)", LEDGER, D16)),
    "les-halles": dict(
        hours=("화–금 06:00–13:30 · 토·일 –14:00", LEDGER, D16),
        closed=("월요일", LEDGER, D16),
        note=("Les Halles 먼저, Palais 나중 순서", LEDGER, D16)),
    "pont-du-gard": dict(
        price_adult=("부지·다리 무료 · 주차 €9/차량 · 실내 전시 €8", LEDGER, D16),
        hours=("9월 09:00–19:00 (매표 18:30 마감)", LEDGER, D16),
        note=("야간 조명 5/15–9/20 운영 (쇼 Les Féeries 는 7/4–8/30 종료)", LEDGER, D16)),
    "pont-saint-benezet": dict(
        price_adult=("통합권(궁+정원+다리) €19.50", LEDGER, D16)),
    "uzes": dict(
        hours=("시장 수·토만", LEDGER, D16),
        note=("무료 셔틀(Mayac↔시내)은 토요일 오전만", LEDGER, D16)),
    "rocher-des-doms": dict(
        hours=("9월 07:30–20:00 (10월 –18:00)", LEDGER, D16)),
    "arles": dict(
        price_adult=("원형경기장+고대극장 €11 · Pass Avantage €19 · Pass Liberté €15", LEDGER, D16),
        note=("JEP 43회 9/19–20 기념물·박물관 무료 (아를 관광청)", LEDGER, D16),
        hours=("", LEDGER, D16, "unreachable",
               "아를 9월 개관시간 공식 페이지 403/404 — 추정값 금지, pending 유지")),
    "cloitre-saint-trophime": dict(
        price_adult=("생트로핌 회랑 €6", LEDGER, D16)),
    "carrieres-des-lumieres": dict(
        hours=("요일 교대 — 피카소·프리다 월·금·일 / 「Océan」 화·수·목·토", LEDGER, D16)),
    "les-baux-de-provence": dict(
        hours=("Château des Baux 9월 09:00–19:00", LEDGER, D16),
        price_adult=("€10 (Carrières 통합권 €21)", LEDGER, D16)),

    # ===== Nice·Côte d'Azur (원장 §3 + CSV) =====
    "colline-du-chateau": dict(
        hours=("4/1–10/31 매일 08:30–20:00", CSV_SRC, D17),
        price_adult=("무료", CSV_SRC, D17),
        note=("공식 페이지에 엘리베이터 언급 없음", CSV_SRC, D17, "unverified",
              None)),
    "marche-de-la-liberation": dict(
        hours=("화–일 06:00–12:30", CSV_SRC, D17),
        closed=("월요일", CSV_SRC, D17)),
    "cours-saleya": dict(
        hours=("화–일 꽃·식품 오전 시장 · 월요일 골동품시장 07:00–18:00", CSV_SRC, D17)),
    "le-rocher": dict(
        note=("위병 교대식 매일 11:55 (Place du Palais)", CSV_SRC, D17)),
    "monaco": dict(
        note=("위병 교대식 매일 11:55 (Place du Palais)", CSV_SRC, D17)),

    # ===== Aix·Marseille (원장 §3 + CSV) =====
    "musee-granet": dict(
        hours=("화–일 10:00–18:00 (~11/1) · 매표 17:30", CSV_SRC, D17),
        closed=("월요일", CSV_SRC, D17),
        price_adult=("일반 €14 / 감액 €12 — 상설 단독권 없음 (McCartney전 포함 단일권)", CSV_SRC, D17)),
    "atelier-des-lauves": dict(
        hours=("7/1–9/30 매일 09:00–18:00 (2026 개방 7/4–10/31)", CSV_SRC, D17),
        price_adult=("€9.50 자율(11:30부터) / €12 가이드 1.5h / €15 심화 2h", CSV_SRC, D17),
        booking=("예약 의무 — places limitées (Réservation obligatoire)", CSV_SRC, D17),
        getting_there=("13 avenue Paul Cézanne, 13090 Aix-en-Provence", CSV_SRC, D17)),
    "mucem": dict(
        closed=("화요일 (+5/1·12/25)", CSV_SRC, D17),
        price_adult=("€11 / 감액 €7.50 / 가족 €18 · 매월 첫 일요일 무료 · 야외 동선 무료", CSV_SRC, D17)),
    "place-richelme-place-des-precheurs": dict(
        hours=("Richelme 식품시장 매일 08:00–13:00 · 화·목·토 큰장(직물·공예·골동)", CSV_SRC, D17)),
    "cassis": dict(
        getting_there=("Gorguettes 셔틀은 9월 주말·방학·공휴일만 운행 — 평일 무효", LEDGER, D16)),
    "saint-paul-de-vence": dict(
        note=("Jason 확정 — 9/8(화) Nice 당일치기로 이설. Aix 챕터에서 제외", LEDGER, D16)),

    # ===== Luberon (CSV) =====
    "abbaye-de-senanque": dict(
        hours=("9월 09:30 개장 · 최종입장 18:30 · 폐장 19:00", CSV_SRC, D17),
        price_adult=("개인 €3.50", CSV_SRC, D17),
        booking=("자유관람 예약 불필요 · 가이드 투어·HistoPad 는 tickeasy 예약", CSV_SRC, D17)),
    "roussillon-sentier-des-ocres": dict(
        hours=("9/1–9/30 09:00–19:00 · 최종입장 30분 전", CSV_SRC, D17),
        price_adult=("성인 €8 · 12–17세 €4 · 12세 미만 무료", CSV_SRC, D17)),
    "gordes": dict(
        hours=("시장 2026 연중 화요일 08:00–13:00", CSV_SRC, D17)),
    "coustellet": dict(
        hours=("생산자시장 매주 일요일 08:00–13:00 (2026-03-29~12-27)", CSV_SRC, D17)),
    "lourmarin": dict(
        hours=("시장 금요일 08:00–13:00 연중 · 일요일 시장 없음", CSV_SRC, D17),
        note=("Lourmarin des Carnets 2026-09-12~13 · 50 carnettistes", CSV_SRC, D17)),

    # ===== Lyon (원장 §3 + CSV) =====
    "halles-de-lyon-paul-bocuse": dict(
        hours=("대부분 상점 월–토 07:30–19:30 · 일 07:30–13:00", CSV_SRC, D17),
        closed=("월요일 다수 점포 휴무", CSV_SRC, D17)),
    "croix-rousse": dict(
        hours=("시장 화·금·토·일 06:00–13:30 (약 95팀) / 수·목 06:00–13:00 (약 23팀)", CSV_SRC, D17),
        closed=("월요일", CSV_SRC, D17)),
    "annecy": dict(
        note=("Novel 시장은 목요일 전용 — 수요일 방문일 대안 불가", LEDGER, D16)),

    # ===== Paris (원장 §3 + CSV) =====
    "musee-du-louvre": dict(
        price_adult=("비EEA €32", LEDGER, D16),
        closed=("화요일", LEDGER, D16)),
    "versailles": dict(
        price_adult=("Passport 고시즌 €35 · 트리아농 €15 · 분수쇼일 정원 €15 (2026-01-14 개정)",
                     LEDGER, D16)),
    "musee-d-orsay": dict(
        hours=("화–일 09:30–18:00 · 목요일 21:45까지 (마지막 입장 21:00)", CSV_SRC, D17),
        closed=("월요일 (+5/1·12/25)", CSV_SRC, D17),
        price_adult=("온라인 €16 / 현장 €14", CSV_SRC, D17)),
    "musee-de-l-orangerie": dict(
        note=("'Monet, painting time' 2026/9/30–2027/1/25 · 금 18시부터 야간 €10 단일가", CSV_SRC, D17),
        price_adult=("", CSV_SRC, D17, "unreachable",
                     "일반 성인 요금·휴관 요일 공식 페이지 403/404 — 확인 실패")),
    "bourse-de-commerce-pinault-collection": dict(
        hours=("월–일 11:00–19:00 · 금요일 21:00까지", CSV_SRC, D17),
        closed=("화요일 (+5/1)", CSV_SRC, D17),
        price_adult=("€15", LEDGER, D16),
        note=("2026/8/26–10/5 전시 준비 기간 · 'Remember Me' 10/7 개막", CSV_SRC, D17)),
    "grand-palais": dict(
        note=("세잔전 2026/9/23–2027/1/17 갤러리 3·4 · 174점 · 예약 2026-07-07 개시", CSV_SRC, D17)),
    "notre-dame-de-paris": dict(
        price_adult=("입장 100% 무료", CSV_SRC, D17),
        booking=("공식 사이트(notredamedeparis.fr)에서만 · 제3자 플랫폼 판매 권한 없음", CSV_SRC, D17)),
    "montmartre-south-pigalle": dict(
        note=("Fête des Vendanges 10/7–11 제93회 · Grande Parade 10/10", CSV_SRC, D17)),

    # ===== Barcelona·Girona (CSV, fact 명 있는 행) =====
    "sagrada-familia": dict(
        price_adult=("기본 €26.00 / 타워 포함 €36.00", "https://sagradafamilia.org/en/prices", D17),
        hours=("일요일 10:30 개장 (4–9월 10:30–20:00)",
               "https://sagradafamilia.org/en/schedules-how-to-get", D17)),
    "sant-pau-recinte-modernista": dict(
        hours=("월–일 09:30–18:30 (4–10월)", CSV_SRC, D17),
        price_adult=("성인 €18 (14시 이전) / €17 (14시 이후)", CSV_SRC, D17)),
    "macba": dict(
        hours=("6/25–9/24 10:00–20:00 · 일 10:00–15:00", CSV_SRC, D17),
        closed=("화요일 (월요일 개관)", CSV_SRC, D17),
        price_adult=("현장 €15.00 · 온라인 €13.50", CSV_SRC, D17)),
    "cau-ferrat": dict(
        hours=("4–10월 화–일 10:00–19:00", CSV_SRC, D17),
        closed=("월요일", CSV_SRC, D17),
        price_adult=("Cau Ferrat + Museu de Maricel 통합권 €12 (3관 통합 €17)", CSV_SRC, D17)),
    "palau-de-maricel": dict(
        hours=("가이드 투어 전용 — 7·8월 화·수 / 9월–6월 일요일만", CSV_SRC, D17),
        price_adult=("별도 €12", CSV_SRC, D17),
        note=("9/1(화) 관람 불가", CSV_SRC, D17)),
    "biblioteca-de-catalunya": dict(
        hours=("", CSV_SRC, D17, "unreachable",
               "공식 사이트(bnc.cat) robots/TLS 차단으로 판독 실패 — 우회 시도 안 함")),
    "collioure": dict(
        hours=("Château Royal 9/1–10/31 10:00–18:00 (마지막 입장 45분 전)", CSV_SRC, D17),
        price_adult=("Château Royal 성인 €9", CSV_SRC, D17),
        note=("전통시장 수·일 오전 Place du Maréchal Leclerc", CSV_SRC, D17)),
    "girona-cathedral": dict(
        hours=("고시즌 6/15–9/15 월–금 10:00–19:00 · 토 –20:00 · 일 12:00–19:00", CSV_SRC, D17),
        price_adult=("대성당+Sant Feliu €7.50 (오디오가이드 포함)", CSV_SRC, D17)),
    "passeig-de-la-muralla": dict(
        hours=("9월–5월 08:00–21:00 (6–8월 –23:00)", CSV_SRC, D17)),
    "pals": dict(
        hours=("시간의 탑 6/15–9/30 수–일 10:30–14:30 / 17:00–20:00", LEDGER, D16),
        note=("점심대(15:20–16:10) 방문 불가", LEDGER, D16)),
    "peralada": dict(
        note=("Jason 확정 — 일정에서 제외 (박물관 투어 예약 안 함)", LEDGER, D16)),
}

# 레지스트리(91)에 spot 으로 없지만 원고가 참조하는 대상 — placeId 를 신규 부여한다.
# (식당·시장·교통·미술관. displayName·region 을 여기서 직접 준다.)
EXTRA_PLACES = {
    # ── Nice 권역 (원장 §3) ──
    "fondation-maeght": ("Fondation Maeght", "nice", dict(
        hours=("9월 10:00–18:00", LEDGER, D16),
        price_adult=("€18 / 감액 €14", LEDGER, D16),
        closed=("2026/9/5·6·7 특별휴관 (9/8 화 정상)", LEDGER, D16),
        getting_there=("직통 없음 — 니스빌→TER 15분→Cagnes-sur-Mer→ZOU! 655번 20–25분→도보 10–12분 급경사 · 구간별 약 €2.10",
                       LEDGER, D16),
        note=("Maeght–Matisse 셔틀 2026 시즌 7/4–8/29 종료 → 9/8 사용 불가", LEDGER, D16))),
    "musee-chagall": ("Musée Chagall", "nice", dict(
        hours=("5/2–10/31 10:00–18:00 연속 개관 (점심 휴관 없음)", LEDGER, D16),
        closed=("화요일", LEDGER, D16),
        price_adult=("특별전 5/23–9/21 기간 €10", LEDGER, D16))),
    "musee-matisse-nice": ("Musée Matisse", "nice", dict(
        closed=("화요일 (Chagall 과 동일 요일)", LEDGER, D16))),
    "musee-picasso-antibes": ("Musée Picasso Antibes", "nice", dict(
        hours=("6/15–9/15 10:00–18:00 연속 · 매표 17:30 마감", LEDGER, D16),
        closed=("월요일 (화–일 개관)", LEDGER, D16),
        price_adult=("€12", LEDGER, D16))),
    "eze": ("Èze", "nice", dict(
        getting_there=("Lignes d'Azur 82번 (Nice Vauban 발) €2.50", LEDGER, D16),
        hours=("Jardin Exotique 9월 09:00–19:30", LEDGER, D16),
        price_adult=("Jardin Exotique €10", LEDGER, D16))),
    "lignes-dazur": ("Lignes d'Azur (Nice 시내교통)", "nice", dict(
        price_adult=("단발 €1.70 (74분 환승 포함) · 1일권 €7 · 7일권 €20", LEDGER, D16),
        note=("구값 €1.80/€5/€15/€40 계열은 전부 오류", LEDGER, D16))),
    "acchiardo": ("Acchiardo", "nice", dict(
        hours=("월–금만 영업", LEDGER, D16),
        closed=("토·일", LEDGER, D16))),
    "marche-provencal-antibes": ("Marché Provençal Antibes", "nice", dict(
        hours=("9월 07:30–13:00", LEDGER, D16),
        closed=("9/1–5/31 월요일 휴무", LEDGER, D16))),

    # ── Avignon 권역 ──
    "hertz-avignon-tgv": ("Hertz Avignon TGV (AVNX92)", "avignon", dict(
        hours=("월–목 08:00–21:00 · 금 –22:00 · 토 09:00–19:00 · 일 10:00–19:00", LEDGER, D16),
        getting_there=("Place de l'Europe · 반납주차 Parking Loueurs P0 · +33 4 32 74 62 80",
                       LEDGER, D16),
        note=("영업시간 외 키드롭 제공 여부·요금·책임은 미확인", LEDGER, D16, "unreachable",
              "Hertz 공식이 키드롭 조건을 게시하지 않음 — 전화 확인 필요"))),
    "virgule-navette": ("TER Virgule (Avignon Centre↔TGV)", "avignon", dict(
        hours=("일요일 08:44 / 09:13 / 10:13 / 10:44 (09:13 권장)", LEDGER, D16),
        price_adult=("€4 · 5–6분", LEDGER, D16),
        note=("'셔틀 없음' 서술은 오류 · Orizo 10번 버스는 일요일 무운행", LEDGER, D16))),
    "taxi-avignon": ("택시 (Avignon Centre→TGV)", "avignon", dict(
        price_adult=("€12–15 · 8–15분 · 24시간", LEDGER, D16),
        booking=("전날 예약 필수", LEDGER, D16))),

    # ── Aix ──
    "piscine-yves-blanc": ("Piscine Yves Blanc", "aix", dict(
        price_adult=("입장 €4 / 감액 €3", CSV_SRC, D17),
        note=("수영모 의무(9/1–6/30) · 수영반바지 금지 · 26 av. des Écoles Militaires",
              CSV_SRC, D17))),
    "rtm-lecar": ("RTM lecar (Aix↔Marseille)", "aix", dict(
        getting_there=("직행(고속도로) 노선 · 1회권 차내 판매 · 90분 환승 유효", CSV_SRC, D17))),

    # ── Luberon ──
    "gout-bistrot": ("Goût Bistrot", "luberon", dict(
        hours=("월 12:00–13:30 · 19:00–21:00 · 금–일 영업", CSV_SRC, D17),
        closed=("수·목", CSV_SRC, D17),
        price_range=("메뉴 €39 / €49", CSV_SRC, D17))),

    # ── Lyon ──
    "musee-des-beaux-arts-lyon": ("Musée des Beaux-Arts", "lyon", dict(
        closed=("화요일", LEDGER, D16))),
    "musee-gadagne": ("Musée Gadagne", "lyon", dict(
        closed=("월·화", LEDGER, D16))),
    "cathedrale-saint-jean": ("Cathédrale Saint-Jean", "lyon", dict(
        hours=("월요일 14:00 개관 (오전 잠김)", LEDGER, D16),
        note=("천문시계 하루 4회 작동", LEDGER, D16))),
    "musee-des-tissus": ("Musée des Tissus", "lyon", dict(
        hours=("", LEDGER, D16, "unreachable",
               "공식은 '폐관 중'만 안내 · 비엔날레 예외 개관 미확인 — 확정 서술 금지"))),
    "tcl": ("TCL (Lyon 시내교통)", "lyon", dict(
        price_adult=("단발 존1-2 €2.10 (1h) · 전존 €3.70 · 24h 존1-2 €6.90 · 전존 24h €9.80 · 푸니쿨라 왕복 €3.60",
                     CSV_SRC, D17))),
    "cafe-comptoir-abel": ("Café Comptoir Abel", "lyon", dict(
        hours=("연중 매일 점심·저녁 (일·월 포함)", CSV_SRC, D17),
        booking=("+33 4 78 37 46 18", CSV_SRC, D17))),
    "daniel-et-denise-crequi": ("Daniel et Denise Créqui", "lyon", dict(
        hours=("월–금 12:00–14:00 / 19:00–22:00", CSV_SRC, D17),
        closed=("토·일", CSV_SRC, D17),
        booking=("+33 4 78 60 66 53", CSV_SRC, D17))),

    # ── Paris ──
    "sacre-coeur": ("Sacré-Cœur", "paris", dict(
        hours=("돔 10:30 개방", LEDGER, D16),
        price_adult=("돔 €8", LEDGER, D16),
        booking=("현장판매만", LEDGER, D16),
        note=("계단 300개", LEDGER, D16))),
    "navigo-idfm": ("Navigo · IDFM (Paris 교통)", "paris", dict(
        price_adult=("Navigo Mois 전존 €90.80 · Semaine €32.40 · 단발 €2.55 (버스·트램 €2.05) · Orly €14 · CDG RER B €7",
                     CSV_SRC, D17),
        note=("2026-01-01 시행 · 구값 €88.80 계열은 오류", CSV_SRC, D17))),
    "arc-de-triomphe-longchamp": ("Prix de l'Arc de Triomphe (Longchamp)", "paris", dict(
        hours=("10/3(토)·10/4(일) 개최 · 본경주 10/4 16:05", CSV_SRC, D17),
        getting_there=("무료 셔틀 Porte Maillot(1호선)·Porte d'Auteuil(10호선) · 토 11:30부터·일 10:30부터 약 15분 간격",
                       CSV_SRC, D17))),

    # ── Barcelona·Girona ──
    "zbe-barcelona": ("ZBE (Barcelona 저배출구역)", "barcelona", dict(
        price_adult=("등록 €5 · €2/일 · 과태료 100유로부터", LEDGER, D16),
        note=("구값 '€7·과태료 €1,800' 은 오류", LEDGER, D16))),
    "aerobus": ("Aerobús", "barcelona", dict(
        price_adult=("", LEDGER, D16, "unreachable",
                     "공식 페이지 판독 실패 · 3자 출처 €7.45 는 미확정 — pending 유지"))),
    "mercat-de-la-concepcio": ("Mercat de la Concepció", "barcelona", dict(
        hours=("월·토 08:00–15:00 · 화–금 08:00–20:00", CSV_SRC, D17))),
    "la-paradeta-sagrada-familia": ("La Paradeta Sagrada Família", "barcelona", dict(
        hours=("화–토 13:00–16:00 / 20:00–23:30 · 일 13:00–16:00", CSV_SRC, D17),
        closed=("월요일", CSV_SRC, D17),
        getting_there=("Passatge Simó 18", CSV_SRC, D17))),
    "bar-canete": ("Bar Cañete", "barcelona", dict(
        hours=("", CSV_SRC, D17, "unreachable",
               "공식 사이트(barcanete.com, /bookings)에 영업시간 미게재 — 추정값 금지"))),
    "mercat-del-lleo": ("Mercat del Lleó", "girona", dict(
        hours=("월–금 07:00–14:00 · 토·공휴일 전날 07:00–14:30", CSV_SRC, D17))),
    "museum-of-jewish-history": ("Museum of Jewish History", "girona", dict(
        hours=("9–6월 화–토 10:00–18:00 · 월·일·공휴일 10:00–14:00", CSV_SRC, D17),
        price_adult=("€6", CSV_SRC, D17))),
    "casa-marieta": ("Casa Marieta", "girona", dict(
        hours=("12:30–15:30 / 19:30–22:30", CSV_SRC, D17, "secondary", None),
        closed=("", CSV_SRC, D17, "unreachable",
                "주간 휴무 요일 공식 미표기 — 화요일 저녁 영업 확정 불가 (전화 확인 필요)"))),
    "la-roca-peratallada": ("La Roca (Peratallada)", "girona", dict(
        hours=("", CSV_SRC, D17, "unreachable",
               "공식 사이트 접속 실패(robots/timeout) · 관광청 venue 페이지에 시간 정보 없음"))),
    "cadaques": ("Cadaqués", "girona", dict(
        getting_there=("Parking Saba Riera Sant Vicenç 실재 (요금·만차 조건 미확인)", CSV_SRC, D17),
        note=("Jason 확정 방문지 — '비추천' 분류 금지", LEDGER, D16))),
    "far-de-tossa": ("Far de Tossa (Tossa de Mar)", "girona", dict(
        price_adult=("€3", LEDGER, D16),
        note=("점심 휴관 있음 · 시립미술관은 개보수 휴관", LEDGER, D16))),
}

# 원장·CSV 에 값이 있으나 placeId 를 확신할 수 없어 적재하지 않은 행
UNMAPPED = [
    ("nice", "월 휴관, 화-일 10:00-18:00 (갤러리동 10:00-12:30/13:30-18:00)", "대상 시설명 없음"),
    ("nice", "화-일 11:30-14:30·17:30-22:00, 월 휴무, 워크인 전용, 13 rue Bavastro", "식당명 없음"),
    ("nice", "니스 관광청 2026 리스팅 주 7일 영업 표기", "대상 없음"),
    ("nice", "9/1-6/30 화-일 07:00-13:00 (월 휴무)", "시장명 없음 (Antibes 추정되나 미확정)"),
    ("nice", "UNVERIFIED — hertz.com 위치 페이지 404", "Hertz Nice 인수지 — 레지스트리 spot 아님"),
    ("aix", "RTM lecar 직행 노선 · 1회권 차내 판매 · 90분 환승", "교통 — 레지스트리 spot 아님"),
    ("aix", "입장 €4/감액 €3 · 수영모 의무 · 26 av. des Écoles Militaires", "Piscine Yves Blanc — spot 아님"),
    ("aix", "매일 07:00–18:00, 주간 휴무 없음", "대상 없음"),
    ("luberon", "월 12:00-13:30·19:00-21:00, 수·목 휴무, 메뉴 39€/49€", "식당명 없음 (Goût Bistrot 추정)"),
    ("avignon", "UNVERIFIED", "대상·내용 모두 없음"),
    ("avignon", "목-월 19:00~, 수요일 휴무. 17 Rue des Trois Faucons", "식당명 없음"),
    ("avignon", "점심 12:00-13:30·저녁 19:30-21:00", "식당명 없음"),
    ("avignon", "공식 사이트에 영업시간 미게시(전화 +33 4 32 76 32 16)", "대상명 없음"),
    ("avignon", "월-금 12:30-13:30·19:15-21:30, 토·일 휴무", "식당명 없음"),
    ("avignon", "2026-09-17(목) 18:00-21:00 Muséum Requien, 무료", "이벤트 — spot 아님"),
    ("avignon", "호텔 공식 'every day' 서술", "대상명 없음"),
    ("avignon", "화 점심-토 저녁 · 21 rue Porte de Laure", "식당명 없음"),
    ("lyon", "연중 매일 점심·저녁 · 04 78 37 46 18", "Café Comptoir Abel 추정 — 식당, spot 아님"),
    ("lyon", "월-금 12-14/19-22 · 04 78 60 66 53", "Daniel et Denise 추정 — 식당, spot 아님"),
    ("lyon", "연중무휴 11:45-14:00/18:45-22:00 · 04 50 45 41 18", "식당명 없음"),
    ("lyon", "연중무휴 7/7 (12-14/18:30-22+)", "식당명 없음"),
    ("lyon", "단발 존1-2 €2.10 · 24h €6.90 · 푸니쿨라 왕복 €3.60", "TCL 교통 — spot 아님"),
    ("lyon", "UNVERIFIED — 9/20 이후 시간표 확인 불가", "대상명 없음"),
    ("paris", "공식 시간표 페이지 404", "대상명 없음"),
    ("paris", "Navigo Semaine €32.40 / Mois €90.80 / 단발 €2.55", "IDFM 교통 — spot 아님"),
    ("paris", "Arc 10/3·10/4 · 본경주 10/4 16:05 · 무료 셔틀", "이벤트 — spot 아님"),
    ("girona", "Casa Marieta 12:30-15:30 / 19:30-22:30", "식당 — spot 아님"),
    ("girona", "Mercat del Lleó 월–금 07:00–14:00", "시장 — spot 아님"),
    ("girona", "Museum of Jewish History 화–토 10:00–18:00 · €6", "spot 미등록"),
    ("girona", "Cadaqués Parking Saba 실재", "Cadaqués spot 미등록 (S1 신규 dossier 대상)"),
    ("girona", "La Roca (Peratallada) UNVERIFIED", "식당 — spot 아님"),
    ("barcelona", "La Paradeta 월요일 휴무 · Passatge Simó 18", "식당 — spot 아님"),
    ("barcelona", "Mercat de la Concepció 월·토 08:00–15:00", "시장 — spot 아님"),
    ("barcelona", "Bar Cañete UNVERIFIED", "식당 — spot 아님"),
]


def main():
    reg = registry()
    places, missing_slug, n_facts = {}, [], 0
    for pid, facts in SEED.items():
        if pid not in reg:
            missing_slug.append(pid)
            continue
        region, name, grade = reg[pid]
        rec = {"displayName": name, "region": region, "grade": grade, "facts": {}}
        for key, tup in facts.items():
            value, source, vat = tup[0], tup[1], tup[2]
            conf = tup[3] if len(tup) > 3 else "official"
            blocked = tup[4] if len(tup) > 4 else None
            if conf == "unverified":
                blocked = None
            rec["facts"][key] = F(value, source, vat, conf, key, blocked)
            n_facts += 1
        places[pid] = rec

    # 레지스트리 미등록 대상 (식당·시장·교통·미술관)
    for pid, (name, region, facts) in EXTRA_PLACES.items():
        if pid in places:
            raise SystemExit(f"placeId 중복: {pid}")
        rec = {"displayName": name, "region": region,
               "grade": reg[pid][2] if pid in reg else "none", "facts": {}}
        for key, tup in facts.items():
            value, source, vat = tup[0], tup[1], tup[2]
            conf = tup[3] if len(tup) > 3 else "official"
            blocked = tup[4] if len(tup) > 4 else None
            if conf in ("unverified", "secondary"):
                blocked = None
            rec["facts"][key] = F(value, source, vat, conf, key, blocked)
            n_facts += 1
        places[pid] = rec

    doc = {"$schema": "./place-facts.schema.json", "version": "1.0",
           "generated": date.today().isoformat(),
           "ttl_defaults": TTL,
           "places": dict(sorted(places.items()))}
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    conf = {}
    for p in places.values():
        for f in p["facts"].values():
            conf[f["confidence"]] = conf.get(f["confidence"], 0) + 1
    print(f"적재: 장소 {len(places)} · 사실 {n_facts}")
    print(f"confidence: {conf}")
    if missing_slug:
        print(f"레지스트리에 없는 slug {len(missing_slug)}: {missing_slug}")
    print(f"UNMAPPED (적재 보류) {len(UNMAPPED)}건 — 소속 placeId 불명 또는 spot 미등록")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
