#!/usr/bin/env python3
"""TP Europe Travel Guidebook — 정적 사이트 빌드 스크립트.

source/ 의 통합 패키지 v1.30(Phase 5 LatestOnly)을
site/ 아래의 순수 정적 HTML 사이트로 변환한다.

콘텐츠 기준 (CURRENT/00_Governance/00_Current_Source_of_Truth_Index_v1.2.md):
 - 본문: 정식 지역 챕터(20_Regional_Chapters) + Core 문서(10_Core)
 - 지도: ASSETS/75_Execution_Maps 8개 지역
 - 데일리 카드: ASSETS/80_Daily_Mobile_Guide_Images 43장 (Day 12–24는 Phase 4 카드 우선)
 - 트래커: OPERATIONS/TP_Europe_Travel_Master_Tracker_v1.1.xlsx

UI/UX 설계: docs/UIUX_Design_v1.0.md
 - '오늘' 버튼 → 당일 데일리 카드 페이지(카드 이미지 + 챕터 일정 + 지역 지도 링크)

사용법:
    python3 build/build.py

필요 패키지: pip install markdown openpyxl
"""

import html
import json
import re
import shutil
import sys
from datetime import date, timedelta
from pathlib import Path

try:
    import markdown
    from markdown.extensions.toc import TocExtension, slugify_unicode
except ImportError:
    sys.exit("markdown 패키지가 필요합니다: pip install markdown")

try:
    import openpyxl
except ImportError:
    sys.exit("openpyxl 패키지가 필요합니다: pip install openpyxl")

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
SITE = ROOT / "site"
ASSETS = ROOT / "build" / "assets"

SITE_TITLE = "Jason과 Julia의 2026 유럽 장기여행 가이드북"
SITE_SHORT = "유럽 43일 가이드북"
TRIP_PERIOD = "2026-08-29 ~ 2026-10-10 · 43일 42박"
TRIP_START = date(2026, 8, 29)
TRIP_END = date(2026, 10, 10)
WEEKDAY_KO = ["월", "화", "수", "목", "금", "토", "일"]

CORE = "CURRENT/10_Core"
REGIONAL = "CURRENT/20_Regional_Chapters"

# 챕터 매니페스트 — kind: intro(안내) / schedule(전체일정) / region(지역 가이드)
CHAPTERS = [
    dict(path=f"{CORE}/01_How_to_Use_This_Guidebook_v1.0.md", slug="01",
         kind="intro", title="가이드북 사용법", sub="읽는 법과 기준 문서"),
    dict(path=f"{CORE}/02_Whole_Trip_Experience_Highlights_v1.0.md", slug="02",
         kind="intro", title="전체 여행 하이라이트", sub="43일의 경험 설계"),
    dict(path=f"{CORE}/03_Whole_Trip_Master_Itinerary_v1.2.md", slug="03",
         kind="schedule", title="43일 Master Itinerary", sub="전체 일정·실행성 감사 반영"),
    dict(path=f"{REGIONAL}/04_Barcelona_Sitges_v1.3.md", slug="04", kind="region",
         title="Barcelona · Sitges", start=date(2026, 8, 29), end=date(2026, 9, 1),
         nights=3, map="barcelona.html", region="Barcelona"),
    dict(path=f"{REGIONAL}/05_Girona_Collioure_Emporda_v1.3.md", slug="05", kind="region",
         title="Girona · Collioure · Empordà", start=date(2026, 9, 1), end=date(2026, 9, 4),
         nights=3, map="girona.html", region="Girona"),
    dict(path=f"{REGIONAL}/06_Nice_Cote_d_Azur_v1.5.md", slug="06", kind="region",
         title="Nice · Côte d’Azur", start=date(2026, 9, 4), end=date(2026, 9, 9),
         nights=5, map="nice.html", region="Nice"),
    dict(path=f"{REGIONAL}/07_Aix_en_Provence_v1.4.md", slug="07", kind="region",
         title="Aix-en-Provence", start=date(2026, 9, 9), end=date(2026, 9, 13),
         nights=4, map="aix.html", region="Aix"),
    dict(path=f"{REGIONAL}/08_Luberon_Farmhouse_v1.5.md", slug="08", kind="region",
         title="Luberon Farmhouse", start=date(2026, 9, 13), end=date(2026, 9, 17),
         nights=4, map="luberon.html", region="Luberon"),
    dict(path=f"{REGIONAL}/09_Avignon_Alpilles_Pont_du_Gard_v1.3.md", slug="09", kind="region",
         title="Avignon · Alpilles · Pont du Gard", start=date(2026, 9, 17), end=date(2026, 9, 21),
         nights=4, map="avignon.html", region="Avignon"),
    dict(path=f"{REGIONAL}/10_Lyon_v1.4.md", slug="10", kind="region",
         title="Lyon · Annecy", start=date(2026, 9, 21), end=date(2026, 9, 25),
         nights=4, map="lyon.html", region="Lyon"),
    dict(path=f"{REGIONAL}/11_Paris_Long_Stay_v1.4.md", slug="11", kind="region",
         title="Paris Long Stay", start=date(2026, 9, 25), end=date(2026, 10, 10),
         nights=15, map="paris.html", region="Paris"),
]

# 실행지도 8종 (ASSETS/75_Execution_Map_Index_v1.0.md 기준)
MAP_DIR = SOURCE / "ASSETS" / "75_Execution_Maps"
MAPS = [
    ("Barcelona_Execution_Map_v0.1.html", "barcelona.html", "Barcelona 실행지도"),
    ("Girona_Execution_Map_v0.1.html", "girona.html", "Girona 실행지도"),
    ("Nice_Execution_Map_v0.1.html", "nice.html", "Nice 실행지도"),
    ("Aix_Execution_Map_v0.1.html", "aix.html", "Aix 실행지도"),
    ("Luberon_Execution_Map_v0.1.html", "luberon.html", "Luberon 실행지도"),
    ("Avignon_Execution_Map_v0.1.html", "avignon.html", "Avignon 실행지도"),
    ("Lyon_Execution_Map_v0.1.html", "lyon.html", "Lyon 실행지도"),
    ("Paris_Execution_Map_v0.1.html", "paris.html", "Paris 실행지도"),
]

# 데일리 모바일 가이드 (ASSETS/80_Daily_Mobile_Guide_Image_Index_v1.1.md 기준)
DAILY_IMG_DIR = SOURCE / "ASSETS" / "80_Daily_Mobile_Guide_Images"
PHASE4_DIR = DAILY_IMG_DIR / "Phase4_Provence_Final"
PHASE4_DAYS = set(range(12, 25))  # Day 12–24는 Phase 4 카드 우선

TRACKER_XLSX = SOURCE / "OPERATIONS" / "TP_Europe_Travel_Master_Tracker_v1.1.xlsx"
TRACKER_SHEETS = [
    ("Master Itinerary", "itinerary", "43일 전체 일정표"),
    ("Reservations", "reservations", "예약 현황"),
    ("Transport", "transport", "이동·교통"),
    ("Accommodation", "accommodation", "숙소 후보·확정"),
    ("Dashboard", "dashboard", "진행 대시보드"),
]

DAY_RE = re.compile(r"Day\s*(\d+)\s*[—\-–]\s*(\d+)월\s*(\d+)일")

# ---------------------------------------------------------------- 분류 체계
# 지역 챕터의 h2 섹션을 카테고리로 재분류·재배치한다.
# 소스는 수정하지 않고 빌드 시 매핑한다 (소스는 상류 콘텐츠 워크플로가 관리).

CATEGORIES = [
    ("intro", "지역소개"),
    ("schedule", "일정"),
    ("info", "여행정보"),
    ("food", "먹거리"),
    ("transport", "교통"),
    ("stay", "숙박"),
    ("booking", "예약"),
    ("cost", "경비"),
    ("tips", "여행팁"),
    ("appendix", "부록"),
]
CAT_LABEL = dict(CATEGORIES)

# 제목 키워드 규칙 — 먼저 맞는 규칙이 이긴다 (번호 접두어 제거 후 적용)
CAT_RULES = [
    ("appendix", r"공식자료|검증 기록|검증 범위|검증 출처|참고 출처|편집 메모|최종 결론|최종 편집 판단|시각요소"),
    ("cost", r"예상 현지비용|예상 경비|^경비"),
    ("booking", r"^예약|예약카드|예약 게이트"),
    ("schedule", r"Day \d|날짜별|일정표|일정 요약|일정 교체|피로도|한눈에 보는|운영 원칙|동선 도식"
                 r"|Quick Reference|실행성 감사|의사결정 게이트|세 사이클|삭제 우선순위"),
    ("transport", r"교통|렌터카|주차|공항|문전 이동|대중교통|자동차|철도"),
    ("stay", r"숙소|생활권|농가"),
    ("intro", r"이해하|어떻게 볼 것인가|도시층|읽는 법|지역 이해|편집자 큐레이션|열쇠"),
    ("food", r"레스토랑|카페|시장|먹어야|식당|장보기|음식|빵|식사체계|먹거리"),
    ("info", r"방문지|관광지|주요 장소|핵심 장소|추천등급|미술관|박물관|도서관|서점|공연|축구"
             r"|근교|체험할|행사|특별전|특별운영|이벤트|선택표|전시"),
    ("tips", r"대체안|확인목록|운동|수영|안전|치안|스케치|지속가능|현장 선택"),
]

# 규칙으로 판별이 어려운 제목의 명시적 지정 (챕터 슬러그, 원문 h2 제목) -> 카테고리
CAT_OVERRIDES = {
    ("05", "시체스에서 지로나 도착, 대성당과 성벽"): "schedule",
    ("05", "콜리우르 시장·왕궁·야수파 산책과 페랄라다"): "schedule",
    ("05", "Pals·Peratallada·Calella de Palafrugell"): "schedule",
    ("05", "지로나에서 니스로 이동"): "schedule",
    ("05", "모듈 A — 동일 차량으로 니스 이동"): "schedule",
    ("05", "모듈 B — 지로나 반납 후 철도 이동"): "schedule",
    ("05", "출발 전 30분 옵션"): "schedule",
    ("05", "5.1 추천 생활권"): "stay",
    ("05", "10.1 로마와 중세 성곽도시"): "intro",
    ("05", "13.1 지로나에서 살 것"): "food",
    ("05", "Jason"): "tips",
    ("05", "Julia"): "tips",
    ("05", "스케치"): "tips",
    ("05", "확정적으로 겹치는 전시"): "info",
    ("05", "9월 2일 행사"): "info",
    ("05", "체류기간 이후"): "info",
    ("05", "지로나"): "transport",
    ("05", "콜리우르"): "transport",
    ("05", "Peratallada·Pals"): "transport",
    ("05", "Calella de Palafrugell"): "transport",
    ("05", "Day 1 비"): "tips",
    ("05", "Day 2 비"): "tips",
    ("05", "Day 3 비"): "tips",
    ("05", "교통지연 기준"): "tips",
    ("05", "Girona Cathedral"): "booking",
    ("05", "Château Royal de Collioure"): "booking",
    ("05", "Museu de Peralada"): "booking",
    ("05", "Day 3 점심"): "booking",
    ("05", "확정"): "booking",
    ("05", "미결정"): "booking",
    ("05", "편집자가 고른 핵심 장소 7곳"): "info",
    ("05", "꼭 체험할 것"): "info",
    ("05", "식당 큐레이션"): "food",
    ("05", "현장 선택 규칙"): "tips",
    ("08", "숙소 평가 최종 기준"): "stay",
    ("10", "치안 판단과 여행 설계 반영"): "tips",
}

NUM_PREFIX_RE = re.compile(r"^\d+[A-Z]?[\.\)]\s*")
SUBNUM_RE = re.compile(r"^\d+\.\d+\s")


def classify(slug, title, prev_cat):
    """h2 섹션 제목을 카테고리로 분류한다."""
    if (slug, title) in CAT_OVERRIDES:
        return CAT_OVERRIDES[(slug, title)]
    if SUBNUM_RE.match(title):        # 7.3 같은 하위번호는 직전 섹션을 따라간다
        return prev_cat or "appendix"
    norm = NUM_PREFIX_RE.sub("", title)
    for cat, pattern in CAT_RULES:
        if re.search(pattern, norm):
            return cat
    return prev_cat or "appendix"

# 빌드 중 수집되는 전역 데이터
CHAPTER_DATE_URL = {}  # 'YYYY-MM-DD' -> 챕터(#Day 앵커) URL — 데일리 페이지에서 사용
DAY_OVERRIDES = {}     # 'YYYY-MM-DD' -> Day 섹션 앵커 URL (범위 매핑보다 우선)
SEARCH_INDEX = []      # {t: 제목, c: 위치, u: URL}


def regroup_regional(slug, body_md):
    """지역 챕터 본문을 카테고리 순서로 재편성한 마크다운을 만든다.

    - 첫 Layer/Pass h1 이전 = 헤더 영역 (제목·부제·도입 인용문). 단 '편집 메모' h2는 부록으로.
    - Layer h1은 제거하고 그 아래 h2들을 개별 분류한다.
    - Pass B/C h1 그룹은 h1을 h2로 낮춰 통째로 '일정'에 넣는다 (내부 h2는 h3로 강등).
    - 각 카테고리는 `# 카테고리명` h1로 시작한다 (서브내비 앵커).
    """
    lines = body_md.splitlines()
    header, sections = [], []   # sections: [title, cat, [lines]]
    cur = None                  # 현재 h2 섹션
    in_header, pass_group = True, False
    prev_cat = None

    def close():
        nonlocal cur
        if cur:
            sections.append(cur)
            cur = None

    for line in lines:
        h1 = re.match(r"^# (.+)", line)
        h2 = re.match(r"^## (.+)", line)
        if h1:
            close()
            title = h1.group(1).strip()
            if re.match(r"Layer\s*\d", title):
                in_header, pass_group = False, False
                cur = ["브리프", "appendix", []]   # h1 직속 내용 임시 수집
                continue
            if re.match(r"Pass\s*[B-Z]", title):
                in_header, pass_group = False, True
                prev_cat = "schedule"
                cur = [title, "schedule", [f"## {title}"]]
                continue
            header.append(line)                    # 챕터 제목 h1
            continue
        if h2:
            title = h2.group(1).strip()
            if in_header:
                close()
                if "편집 메모" in title:
                    cur = [title, "appendix", [line]]
                else:
                    header.append(line)   # 부제 h2 — cur가 None이므로 후속 줄도 헤더로
                continue
            if pass_group:
                cat = CAT_OVERRIDES.get((slug, title))
                if cat is None:
                    close()
                    cur = [title, "schedule", [f"### {title}"]]
                    prev_cat = "schedule"
                    continue
                pass_group_cat = cat
                close()
                cur = [title, pass_group_cat, [line]]
                prev_cat = pass_group_cat
                continue
            cat = classify(slug, title, prev_cat)
            close()
            cur = [title, cat, [line]]
            prev_cat = cat
            continue
        if cur is not None:
            cur[2].append(line)
        elif in_header:
            header.append(line)
    close()

    # 빈 '브리프' 의사섹션 제거, 내용 있으면 부록으로
    sections = [s for s in sections
                if not (s[0] == "브리프" and not any(x.strip() for x in s[2]))]

    # 소스에 경비 섹션이 없는 챕터에는 트래커로 안내하는 스텁을 넣어 메뉴를 일관되게 유지
    if not any(s[1] == "cost" for s in sections):
        sections.append(["경비 안내", "cost", [
            "## 경비 참고처",
            "",
            "이 지역 챕터의 소스에는 아직 별도 경비 정리가 없다. 다음을 참고한다.",
            "",
            "- 숙박 예산: 위 **숙박** 카테고리의 숙소 전략·예산 항목",
            "- 전체 예산과 예약 지출: [진행 대시보드](../tracker/dashboard.html) · [예약 현황](../tracker/reservations.html)",
            "- 입장료·식비 기준: 본문 각 장소·식당 항목의 가격 표기",
        ]])

    out = header[:]
    counts = {}
    for key, label in CATEGORIES:
        matched = [s for s in sections if s[1] == key]
        if not matched:
            continue
        counts[label] = len(matched)
        out += ["", f"# {label}", ""]
        for s in matched:
            out += s[2] + [""]
    unknown = [s[0] for s in sections if s[1] not in CAT_LABEL]
    if unknown:
        print(f"  경고: 미분류 섹션({slug}): {unknown}")
        sys.exit(1)
    return "\n".join(out), counts


# ---------------------------------------------------------------- 장소 큐레이션
# 여행정보 카테고리 상단의 '주요 방문지' 카드. 이름·설명은 큐레이션, 좌표·Google Maps
# 링크는 실행지도 geojson/html에서 가져온다. 사진은 열람 시 브라우저가 Wikipedia
# REST API에서 불러오는 점진적 향상 방식 (오프라인·실패 시 자동 숨김).
PLACES = {
    "04": [
        ("Sagrada Família", "Sagrada Família", "en", "가우디 필생의 성당 — 1882년 착공해 지금도 건축 중"),
        ("Sant Pau", "Hospital de Sant Pau", "en", "세계문화유산 모데르니스메 병원 단지"),
        ("Gòtic", "Gothic Quarter, Barcelona", "en", "로마 성벽 위에 쌓인 중세 고딕 지구"),
        ("Biblioteca de Catalunya", "Biblioteca de Catalunya", "en", "15세기 병원 건물에 들어선 카탈루냐 도서관"),
        ("MACBA", "Museu d'Art Contemporani de Barcelona", "en", "라발 지구의 현대미술관"),
        ("Barcelona Sants", "Barcelona Sants railway station", "en", "고속철·근교선이 모이는 중앙역"),
        ("Sitges", "Sitges", "en", "해변·구시가·미술관의 휴양 소도시"),
    ],
    "05": [
        ("Girona Cathedral", "Girona Cathedral", "en", "세계에서 가장 넓은 고딕 신랑을 가진 대성당"),
        ("Onyar Houses", "Onyar", "en", "오냐르 강변의 색색 파사드와 붉은 철교"),
        ("Collioure", "Collioure", "en", "야수파 화가들이 사랑한 프랑스 카탈루냐 항구마을"),
        ("Peralada", "Peralada", "en", "성과 와이너리의 엠포르다 귀족 마을"),
        ("Pals", "Pals", "en", "엠포르다 평야를 내려다보는 중세 석조마을"),
        ("Peratallada", "Peratallada", "en", "돌을 깎아 만든 해자와 요새의 마을"),
        ("Calella de Palafrugell", "Calella de Palafrugell", "en", "코스타브라바의 어촌 해변마을"),
    ],
    "06": [
        ("Cours Saleya", "Cours Saleya", "en", "니스 구시가의 식품·꽃 시장 거리"),
        ("Castle Hill", "Castle Hill, Nice", "en", "천사의 만과 항구를 내려다보는 전망 언덕"),
        ("Nice-Ville", "Gare de Nice-Ville", "en", "칸·모나코행 TER이 출발하는 중앙역"),
        ("Cannes", "Cannes", "en", "영화제의 도시 — 르 쉬케 언덕과 크루아제트"),
        ("Monaco", "Monaco", "en", "왕궁과 몬테카를로의 도시국가"),
        ("Libération Market", None, "en", "현지 생활형 아침시장 — 9/8 회복일의 장보기"),
        ("NCE T2", "Nice Côte d'Azur Airport", "en", "9/9 렌터카 인수 지점 (Terminal 2)"),
    ],
    "07": [
        ("Rotonde", "Fontaine de la Rotonde", "en", "미라보 대로 초입의 대분수 로터리"),
        ("Cours Mirabeau", "Cours Mirabeau", "en", "플라타너스 그늘이 덮는 엑상의 중심 산책로"),
        ("Musée Granet", "Musée Granet", "en", "세잔과 유럽 회화의 미술관"),
        ("Cassis", "Cassis", "en", "칼랑크 석회암 절벽 아래의 항구마을"),
        ("Atelier Cézanne", "Atelier de Cézanne", "fr", "세잔이 말년을 보낸 아틀리에"),
        ("Lourmarin", "Lourmarin", "en", "카뮈가 잠든 뤼베롱 초입 마을 — 9/13 경유"),
    ],
    "08": [
        ("Coustellet", None, "en", "농산물 직판장이 서는 교차 마을"),
        ("Roussillon", "Roussillon, Vaucluse", "en", "오커 채석장의 붉은 절벽 마을"),
        ("Goult", "Goult", "en", "조용한 언덕 위 와인 마을"),
        ("Gordes", "Gordes", "en", "절벽에 쌓아 올린 뤼베롱의 대표 석조마을"),
        ("Village des Bories", "Village des Bories", "fr", "돌로만 쌓은 옛 농경 오두막 마을"),
        ("Ménerbes", "Ménerbes", "en", "『프로방스에서의 1년』의 무대"),
        ("L’Isle-sur-la-Sorgue", "L'Isle-sur-la-Sorgue", "en", "물레방아와 골동품 시장의 수상 마을"),
    ],
    "09": [
        ("Les Halles", "Les Halles d'Avignon", "fr", "아비뇽의 실내 중앙시장"),
        ("Palais des Papes", "Palais des Papes", "en", "14세기 교황들이 머문 거대한 궁전"),
        ("Pont Saint-Bénézet", "Pont Saint-Bénézet", "en", "노래로 남은 론 강의 끊어진 다리"),
        ("Uzès", "Uzès", "en", "토요시장이 유명한 공작령 도시"),
        ("Pont du Gard", "Pont du Gard", "en", "로마 수도교 — 세계문화유산"),
        ("Les Baux", "Les Baux-de-Provence", "en", "석회암 바위산 위의 요새 마을"),
        ("Saint-Rémy", "Saint-Rémy-de-Provence", "en", "고흐가 요양하며 그림을 그린 마을"),
    ],
    "10": [
        ("Bellecour", "Place Bellecour", "en", "유럽 최대급 광장 — 리옹의 중심"),
        ("Fourvière", "Basilica of Notre-Dame de Fourvière", "en", "도시를 내려다보는 언덕 위 대성당"),
        ("Vieux Lyon", "Vieux Lyon", "en", "르네상스 골목과 트라불의 구시가"),
        ("Croix-Rousse", "La Croix-Rousse", "en", "비단직공의 언덕 동네"),
        ("Halles Paul Bocuse", "Les Halles de Lyon-Paul Bocuse", "en", "미식도시 리옹의 실내 시장"),
        ("Parc Tête d’Or", "Parc de la Tête d'or", "en", "호수가 있는 대공원 — 러닝 코스"),
        ("Annecy", "Annecy", "en", "알프스 호수와 운하의 도시 — 당일치기"),
    ],
    "11": [
        ("Notre-Dame", "Notre-Dame de Paris", "en", "복원을 마친 시테섬의 대성당"),
        ("Louvre", "Louvre", "en", "세계 최대의 미술관"),
        ("Montmartre", "Montmartre", "en", "사크레쾨르와 화가들의 언덕"),
        ("BnF Richelieu", "Bibliothèque nationale de France", "en", "리슐리외 열람실의 국립도서관"),
        ("Grand Palais", "Grand Palais", "en", "특별전이 열리는 대전시장"),
        ("Orsay", "Musée d'Orsay", "en", "기차역을 개조한 인상파 미술관"),
        ("Bourse de Commerce", "Bourse de Commerce", "en", "피노 컬렉션의 현대미술관"),
        ("Versailles", "Palace of Versailles", "en", "절대왕정의 궁전과 정원 — 근교 옵션"),
        ("Giverny", "Giverny", "en", "모네의 정원 마을 — 근교 옵션"),
    ],
}


def load_map_links():
    """실행지도 HTML에서 장소별 Google Maps 링크를 추출한다."""
    links = {}
    for src_name, _, _ in MAPS:
        text = (MAP_DIR / src_name).read_text(encoding="utf-8")
        m = re.search(r"const pts=(\[.*?\]);", text, re.S)
        if m:
            for pt in json.loads(m.group(1)):
                links[pt["name"]] = pt.get("url", "")
    return links


def places_block(chapter, map_links):
    """여행정보 카테고리 상단의 주요 방문지 카드 HTML."""
    places = PLACES.get(chapter["slug"])
    if not places:
        return ""
    cards = []
    for name, wiki, lang, desc in places:
        gmaps = map_links.get(name) or (
            "https://www.google.com/maps/search/?api=1&query=" + name.replace(" ", "+"))
        wiki_attr = (f' data-wiki="{html.escape(wiki, quote=True)}" data-wlang="{lang}"'
                     if wiki else "")
        cards.append(f"""<div class="pl-card"{wiki_attr}>
  <div class="pl-photo" hidden><img alt="{html.escape(name)}" loading="lazy"><a class="pl-credit"
    target="_blank" rel="noopener" href="#">사진: Wikipedia</a></div>
  <div class="pl-body">
    <b>{html.escape(name)}</b>
    <p>{html.escape(desc)}</p>
    <div class="pl-links"><a target="_blank" rel="noopener" href="{html.escape(gmaps)}">Google Maps</a>
    <a href="../maps/{chapter["map"]}">실행지도</a></div>
  </div>
</div>""")
    return ('<section class="places"><h3>주요 방문지</h3>'
            '<p class="note">사진은 온라인 상태에서 Wikipedia로부터 불러옵니다.</p>'
            f'<div class="pl-grid">{"".join(cards)}</div></section>')


# ---------------------------------------------------------------- utilities

def parse_frontmatter(text):
    """단순 YAML frontmatter를 dict로 파싱하고 본문을 돌려준다."""
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    key, _, value = line.partition(":")
                    meta[key.strip()] = value.strip().strip('"')
            text = text[end + 4:]
    return meta, text.lstrip("\n")


def md_convert(text):
    md = markdown.Markdown(
        extensions=["tables", "fenced_code",
                    TocExtension(slugify=slugify_unicode, toc_depth="1-3")],
        output_format="html5",
    )
    body = md.convert(text)
    return body, md.toc_tokens


def flatten_tokens(tokens):
    flat = []
    for tok in tokens:
        flat.append(tok)
        flat.extend(flatten_tokens(tok.get("children", [])))
    return flat


def wrap_tables(body):
    body = body.replace("<table>", '<div class="table-wrap"><table>')
    return body.replace("</table>", "</table></div>")


def mark_layer_headings(body):
    """카테고리 경계 h1에 시각 구분용 클래스를 부여한다."""
    labels = "|".join(label for _, label in CATEGORIES)
    return re.sub(rf'<h1 id="([^"]*)">({labels})</h1>',
                  r'<h1 id="\1" class="layer-h">\2</h1>', body)


def rewrite_md_links(body, slug_by_file):
    def repl(match):
        name = Path(match.group(1).split("#")[0]).name
        if name in slug_by_file:
            return f'href="{slug_by_file[name]}.html"'
        return match.group(0)
    return re.sub(r'href="([^"]+\.md)"', repl, body)


def toc_html(tokens):
    items = []
    for tok in tokens:
        items.append(f'<li><a href="#{tok["id"]}">{html.escape(tok["name"])}</a></li>')
        for child in tok.get("children", []):
            items.append(
                f'<li class="toc-sub"><a href="#{child["id"]}">{html.escape(child["name"])}</a></li>')
    if not items:
        return ""
    return ('<details class="toc"><summary>전체 목차</summary><ul>'
            + "".join(items) + "</ul></details>")


def date_label(d):
    return f"{d.month}/{d.day}"


def day_no(d):
    return (d - TRIP_START).days + 1


def date_of_day(n):
    return TRIP_START + timedelta(days=n - 1)


def chapter_for_date(d):
    """해당 날짜의 지역 챕터 (경계일은 도착 챕터)."""
    for c in reversed([c for c in CHAPTERS if c["kind"] == "region"]):
        if c["start"] <= d <= c["end"]:
            return c
    return None


# ---------------------------------------------------------------- page shell

def drawer_html(rel):
    intro = "".join(
        f'<a href="{rel}/chapters/{c["slug"]}.html">{c["slug"]} {c["title"]}</a>'
        for c in CHAPTERS if c["kind"] != "region")
    regions = "".join(
        f'<a href="{rel}/chapters/{c["slug"]}.html">{c["slug"]} {c["title"]}'
        f'<span>{date_label(c["start"])}–{date_label(c["end"])} · {c["nights"]}박</span></a>'
        for c in CHAPTERS if c["kind"] == "region")
    maps = "".join(
        f'<a href="{rel}/maps/{out}">{title}</a>' for _, out, title in MAPS)
    tracker = "".join(
        f'<a href="{rel}/tracker/{slug}.html">{label}</a>'
        for _, slug, label in TRACKER_SHEETS)
    return f"""<div id="overlay"></div>
<aside id="drawer" aria-label="전체 메뉴">
  <div class="dw-head">
    <span>{SITE_SHORT}</span>
    <button id="drawer-close" aria-label="닫기">✕</button>
  </div>
  <input id="search-input" type="search" placeholder="장소·섹션 검색" autocomplete="off">
  <div id="search-results"></div>
  <nav class="dw-nav">
    <a href="{rel}/index.html" class="dw-home">🏠 홈 — 여정 타임라인</a>
    <a href="{rel}/daily/index.html" class="dw-home">🗓️ 데일리 가이드 — 43일 카드</a>
    <h3>시작하기</h3>{intro}
    <h3>지역 가이드</h3>{regions}
    <h3>실행지도</h3>{maps}
    <h3>트래커</h3>{tracker}
  </nav>
</aside>"""


def page(title, body, *, rel="..", topbar_title=None, meta_line="", subnav=""):
    meta_html = f'<p class="meta">{meta_line}</p>' if meta_line else ""
    tb_title = html.escape(topbar_title or title)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} — {SITE_TITLE}</title>
<link rel="stylesheet" href="{rel}/assets/style.css">
</head>
<body data-rel="{rel}">
<header class="topbar">
  <button id="menu-btn" aria-label="메뉴 열기">☰</button>
  <a class="tb-title" href="{rel}/index.html">{tb_title}</a>
  <nav class="tb-links">
    <a href="{rel}/chapters/03.html">일정</a>
    <a href="{rel}/maps/index.html">지도</a>
    <a href="{rel}/tracker/index.html">트래커</a>
  </nav>
</header>
{subnav}
{drawer_html(rel)}
<main>
{meta_html}
{body}
</main>
<footer>
  <p>{SITE_TITLE} · {TRIP_PERIOD}</p>
</footer>
<nav class="bottomnav" aria-label="주요 메뉴">
  <a href="{rel}/index.html"><b>🏠</b><span>홈</span></a>
  <a href="{rel}/chapters/03.html"><b>📅</b><span>일정</span></a>
  <a href="#" class="nav-today"><b>📍</b><span>오늘</span></a>
  <a href="{rel}/maps/index.html"><b>🗺️</b><span>지도</span></a>
  <a href="{rel}/tracker/index.html"><b>📋</b><span>트래커</span></a>
</nav>
<button id="back-top" aria-label="맨 위로">↑</button>
<script src="{rel}/assets/data.js" defer></script>
<script src="{rel}/assets/nav.js" defer></script>
</body>
</html>
"""


# ---------------------------------------------------------------- chapters

def chapter_subnav(chapter, flat_tokens):
    """카테고리 점프 + Day 칩 서브내비 (지역 챕터 전용)."""
    labels = {label for _, label in CATEGORIES}
    cats, days, seen_days = [], [], set()
    for tok in flat_tokens:
        if tok["level"] == 1 and tok["name"] in labels:
            cats.append(f'<a href="#{tok["id"]}">{tok["name"]}</a>')
        dm = DAY_RE.search(tok["name"])
        if dm and dm.group(1) not in seen_days:
            seen_days.add(dm.group(1))
            days.append(f'<a href="#{tok["id"]}" title="{html.escape(tok["name"])}">'
                        f'{int(dm.group(2))}/{int(dm.group(3))}</a>')
    if not cats and not days:
        return ""
    cats_html = f'<div class="sn-layers">{"".join(cats)}</div>' if cats else ""
    days_html = f'<div class="sn-days">{"".join(days)}</div>' if days else ""
    return f'<nav class="subnav">{cats_html}{days_html}</nav>'


def related_box(chapter):
    """지역 챕터 상단의 관련 리소스 링크."""
    if chapter["kind"] != "region":
        return ""
    links = [f'<a href="../maps/{chapter["map"]}">🗺️ {chapter["region"]} 실행지도</a>',
             f'<a href="../daily/day-{day_no(chapter["start"]):02d}.html">🗓️ 데일리 카드</a>',
             '<a href="../tracker/reservations.html">📋 예약 현황</a>',
             '<a href="../chapters/03.html">📅 43일 일정표</a>']
    return f'<div class="related">{"".join(links)}</div>'


def collect_search(chapter, flat_tokens):
    label = f'{chapter["slug"]} {chapter["title"]}'
    SEARCH_INDEX.append({"t": chapter["title"], "c": f'챕터 {chapter["slug"]}',
                         "u": f'chapters/{chapter["slug"]}.html'})
    for tok in flat_tokens:
        name = tok["name"].strip()
        if not name or name.startswith(("Layer", "Pass")):
            continue
        SEARCH_INDEX.append({"t": name, "c": label,
                             "u": f'chapters/{chapter["slug"]}.html#{tok["id"]}'})


def collect_chapter_dates(chapter, flat_tokens):
    """날짜 → 챕터 URL 매핑. 지역 범위로 채우고 Day 섹션 앵커는 별도 수집."""
    if chapter["kind"] != "region":
        return
    url = f'chapters/{chapter["slug"]}.html'
    d = chapter["start"]
    last = chapter["end"] if chapter["slug"] == "11" else chapter["end"] - timedelta(days=1)
    while d <= last:
        CHAPTER_DATE_URL[d.isoformat()] = url
        d += timedelta(days=1)
    for tok in flat_tokens:
        dm = DAY_RE.search(tok["name"])
        if dm:
            day_date = date(2026, int(dm.group(2)), int(dm.group(3)))
            DAY_OVERRIDES[day_date.isoformat()] = f'{url}#{tok["id"]}'


def build_chapters():
    out_dir = SITE / "chapters"
    out_dir.mkdir(parents=True, exist_ok=True)
    slug_by_file = {Path(c["path"]).name: c["slug"] for c in CHAPTERS}
    map_links = load_map_links()

    for i, c in enumerate(CHAPTERS):
        text = (SOURCE / c["path"]).read_text(encoding="utf-8")
        meta, body_md = parse_frontmatter(text)
        if c["kind"] == "region":
            body_md, counts = regroup_regional(c["slug"], body_md)
        body, toc_tokens = md_convert(body_md)
        flat = flatten_tokens(toc_tokens)
        body = mark_layer_headings(wrap_tables(rewrite_md_links(body, slug_by_file)))
        if c["kind"] == "region":
            # 여행정보 카테고리 첫머리에 주요 방문지 카드 삽입
            info_h1 = re.search(r'<h1 id="[^"]*" class="layer-h">여행정보</h1>', body)
            if info_h1:
                body = (body[:info_h1.end()] + places_block(c, map_links)
                        + body[info_h1.end():])

        collect_search(c, flat)
        collect_chapter_dates(c, flat)

        meta_bits = []
        if c["kind"] == "region":
            meta_bits.append(f'{date_label(c["start"])} ~ {date_label(c["end"])} · {c["nights"]}박')
        if meta.get("version"):
            meta_bits.append(f'v{meta["version"]}')

        prev_link = next_link = ""
        if i > 0:
            p = CHAPTERS[i - 1]
            prev_link = f'<a href="{p["slug"]}.html">← {p["title"]}</a>'
        if i < len(CHAPTERS) - 1:
            n = CHAPTERS[i + 1]
            next_link = f'<a href="{n["slug"]}.html">{n["title"]} →</a>'
        pager = f'<nav class="pager">{prev_link}<span></span>{next_link}</nav>'

        content = related_box(c) + toc_html(toc_tokens) + body + pager
        (out_dir / f'{c["slug"]}.html').write_text(
            page(c["title"], content, rel="..",
                 topbar_title=f'{c["slug"]} · {c["title"]}',
                 meta_line=" · ".join(meta_bits),
                 subnav=chapter_subnav(c, flat)),
            encoding="utf-8")
        cat_info = ("  [" + " ".join(f"{k}:{v}" for k, v in counts.items()) + "]"
                    if c["kind"] == "region" else "")
        print(f'  챕터 {c["slug"]}: {Path(c["path"]).name} → chapters/{c["slug"]}.html{cat_info}')


# ---------------------------------------------------------------- daily cards

def find_daily_images():
    """Day 번호 → 카드 이미지 경로. Day 12–24는 Phase 4 카드를 우선한다."""
    images = {}
    for f in sorted(DAILY_IMG_DIR.glob("Day_*.png")):
        m = re.match(r"Day_(\d+)_(.+)\.png", f.name)
        if m:
            images[int(m.group(1))] = {"src": f, "region": m.group(2).replace("_", " ")}
    for f in sorted(PHASE4_DIR.glob("Day_*_Phase4_v1.0.png")):
        m = re.match(r"Day_(\d+)_(.+)_Phase4_v1\.0\.png", f.name)
        if m and int(m.group(1)) in PHASE4_DAYS:
            images[int(m.group(1))] = {"src": f, "region": m.group(2).replace("_", " "),
                                       "phase4": True}
    return images


def build_daily():
    out_dir = SITE / "daily"
    img_dir = out_dir / "img"
    img_dir.mkdir(parents=True, exist_ok=True)
    images = find_daily_images()

    missing = [n for n in range(1, 44) if n not in images]
    if missing:
        print("데일리 카드 누락:", missing)
        sys.exit(1)

    index_items = []
    for n in range(1, 44):
        d = date_of_day(n)
        info = images[n]
        shutil.copy(info["src"], img_dir / f"day-{n:02d}.png")
        c = chapter_for_date(d)
        wd = WEEKDAY_KO[d.weekday()]
        title = f"Day {n} · {date_label(d)} {wd} · {info['region']}"

        ch_url = CHAPTER_DATE_URL.get(d.isoformat(), "chapters/03.html")
        links = [f'<a href="../{ch_url}">📖 이날의 챕터 일정</a>']
        if c:
            links.append(f'<a href="../maps/{c["map"]}">🗺️ {c["region"]} 실행지도</a>')
        links.append('<a href="index.html">🗓️ 전체 데일리 목록</a>')

        prev_link = f'<a href="day-{n-1:02d}.html">← Day {n-1}</a>' if n > 1 else ""
        next_link = f'<a href="day-{n+1:02d}.html">Day {n+1} →</a>' if n < 43 else ""
        pager = f'<nav class="pager">{prev_link}<span></span>{next_link}</nav>'
        badge = ' <span class="p4-badge">Phase 4 최종</span>' if info.get("phase4") else ""

        body = f"""<h1>{title}{badge}</h1>
<div class="related">{''.join(links)}</div>
<figure class="daily-card"><img src="img/day-{n:02d}.png"
  alt="{title} 데일리 모바일 가이드 카드" loading="lazy"></figure>
<p class="note">카드의 지도영역은 일정 순서를 보여주는 개요이며 내비게이션이 아닙니다.
실제 도보·운전 경로는 Google Maps에서 다시 계산하세요.</p>
{pager}"""
        (out_dir / f"day-{n:02d}.html").write_text(
            page(title, body, rel="..", topbar_title=title), encoding="utf-8")

        index_items.append(
            f'<a class="daily-item" href="day-{n:02d}.html">'
            f'<b>Day {n}</b><span>{date_label(d)} {wd}</span>'
            f'<span class="di-region">{info["region"]}</span></a>')
        SEARCH_INDEX.append({"t": title, "c": "데일리 가이드", "u": f"daily/day-{n:02d}.html"})

    body = ('<h1>데일리 가이드 — 43일 카드</h1>'
            '<p class="meta">일자별 세로형 모바일 가이드 카드 (1080×1920) · '
            'Day 12–24는 Phase 4 최종판</p>'
            f'<div class="daily-grid">{"".join(index_items)}</div>')
    (out_dir / "index.html").write_text(
        page("데일리 가이드", body, rel="..", topbar_title="데일리 가이드"),
        encoding="utf-8")
    print(f"  데일리 카드: 43일 → daily/day-01~43.html (Phase4 적용 {len(PHASE4_DAYS)}일)")


# ---------------------------------------------------------------- home

def build_home():
    stops = []
    for c in CHAPTERS:
        if c["kind"] != "region":
            continue
        stops.append(f"""<li>
  <div class="tl-dates">{date_label(c["start"])} – {date_label(c["end"])}<b>{c["nights"]}박</b></div>
  <div class="tl-body">
    <a class="tl-title" href="chapters/{c["slug"]}.html">{c["title"]}</a>
    <a class="tl-map" href="maps/{c["map"]}">지도</a>
  </div>
</li>""")

    intro_cards = "".join(
        f'<a class="card" href="chapters/{c["slug"]}.html">'
        f'<span class="card-num">{c["slug"]}</span>'
        f'<span class="card-title">{c["title"]}</span>'
        f'<span class="card-sub">{c["sub"]}</span></a>'
        for c in CHAPTERS if c["kind"] != "region")

    tool_cards = (
        '<a class="card card-alt" href="daily/index.html">'
        '<span class="card-num">🗓️</span><span class="card-title">데일리 가이드</span>'
        '<span class="card-sub">43일 모바일 카드 · 하루 한 장</span></a>'
        '<a class="card card-alt" href="maps/index.html">'
        '<span class="card-num">🗺️</span><span class="card-title">실행지도 8종</span>'
        '<span class="card-sub">지역별 기준점 · Google Maps 연동</span></a>'
        '<a class="card card-alt" href="tracker/index.html">'
        '<span class="card-num">📋</span><span class="card-title">마스터 트래커</span>'
        '<span class="card-sub">일정 · 예약 · 이동 · 숙소 · 대시보드</span></a>')

    body = f"""<section class="hero">
  <h1>{SITE_TITLE}</h1>
  <p class="period">{TRIP_PERIOD}</p>
  <a href="#" class="nav-today btn-today">📍 오늘 일정 열기</a>
</section>
<h2>여정</h2>
<ol class="timeline">{''.join(stops)}</ol>
<h2>시작하기</h2>
<div class="grid">{intro_cards}</div>
<h2>도구</h2>
<div class="grid">{tool_cards}</div>
<p class="note">지도 배경 타일은 인터넷 연결 시 표시됩니다. 본문·데일리 카드·마커 목록은 오프라인에서도 열람됩니다.</p>
"""
    (SITE / "index.html").write_text(
        page("홈", body, rel=".", topbar_title=SITE_SHORT), encoding="utf-8")
    print("  홈 → index.html")


# ---------------------------------------------------------------- maps

def build_maps():
    out_dir = SITE / "maps"
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ASSETS / "vendor" / "leaflet", out_dir / "vendor" / "leaflet",
                    dirs_exist_ok=True)
    cards = []
    for src_name, out_name, title in MAPS:
        text = (MAP_DIR / src_name).read_text(encoding="utf-8")
        text = text.replace(
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css", "vendor/leaflet/leaflet.css")
        text = text.replace(
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js", "vendor/leaflet/leaflet.js")
        back = ('<a href="../maps/index.html" style="position:absolute;z-index:1100;right:12px;top:12px;'
                'background:#1f4e78;color:#fff;padding:7px 12px;border-radius:8px;'
                'font-size:13px;text-decoration:none;box-shadow:0 1px 6px rgba(0,0,0,.3)">← 지도 목록</a>')
        text = text.replace('<div id="map"></div>', f'<div id="map"></div>{back}', 1)
        (out_dir / out_name).write_text(text, encoding="utf-8")
        cards.append(f'<a class="card card-alt" href="{out_name}">'
                     f'<span class="card-num">🗺️</span><span class="card-title">{title}</span>'
                     f'<span class="card-sub">주요 기준점 · Google Maps 연동</span></a>')
        SEARCH_INDEX.append({"t": title, "c": "실행지도", "u": f"maps/{out_name}"})
    print(f"  지도: {len(MAPS)}개 지역 → maps/")

    body = ('<h1>실행지도</h1>'
            '<p class="meta">지역별 주요 기준점 지도. 마커를 누르면 Google Maps 검색이 열린다. '
            '배경 타일은 인터넷 연결 시 표시된다.</p>'
            f'<div class="grid">{"".join(cards)}</div>')
    (out_dir / "index.html").write_text(
        page("실행지도", body, rel=".."), encoding="utf-8")


# ---------------------------------------------------------------- tracker

def format_cell(v):
    if v is None:
        return ""
    if hasattr(v, "hour"):  # datetime — 시각이 00:00이면 날짜만
        if (v.hour, v.minute, v.second) == (0, 0, 0):
            return v.strftime("%Y-%m-%d")
        return v.strftime("%Y-%m-%d %H:%M")
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def sheet_to_table(ws):
    rows = []
    for row in ws.iter_rows(values_only=True):
        cells = [format_cell(v) for v in row]
        if any(c.strip() for c in cells):
            rows.append(cells)
    if not rows:
        return ""
    # 선두의 제목 행(비어 있지 않은 셀이 1개뿐)은 캡션으로 분리
    captions = []
    while rows and sum(1 for c in rows[0] if c.strip()) == 1:
        captions.append(next(c for c in rows[0] if c.strip()))
        rows.pop(0)
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    keep = [i for i in range(width) if any(r[i].strip() for r in rows)]
    rows = [[r[i] for i in keep] for r in rows]

    head = "".join(f"<th>{html.escape(c)}</th>" for c in rows[0])
    body_rows = []
    for r in rows[1:]:
        body_rows.append("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>")
    caption_html = "".join(f'<p class="meta">{html.escape(c)}</p>' for c in captions)
    return (f'{caption_html}<div class="table-wrap"><table><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body_rows)}</tbody></table></div>')


def build_tracker():
    out_dir = SITE / "tracker"
    out_dir.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.load_workbook(TRACKER_XLSX, data_only=True)

    def tabs_of(active):
        links = []
        for _, s, label in TRACKER_SHEETS:
            cls = ' class="active"' if s == active else ""
            links.append(f'<a href="{s}.html"{cls}>{label}</a>')
        return '<nav class="tabs">' + "".join(links) + "</nav>"

    cards = []
    for sheet_name, slug, label in TRACKER_SHEETS:
        if sheet_name not in wb.sheetnames:
            print(f"  경고: 시트 없음 — {sheet_name}")
            continue
        table = sheet_to_table(wb[sheet_name])
        body = f"<h1>{label}</h1>{tabs_of(slug)}{table}"
        (out_dir / f"{slug}.html").write_text(
            page(label, body, rel="..", topbar_title=f"트래커 · {label}",
                 meta_line="TP_Europe_Travel_Master_Tracker_v1.1.xlsx 기준"),
            encoding="utf-8")
        cards.append(f'<a class="card card-alt" href="{slug}.html">'
                     f'<span class="card-title">{label}</span>'
                     f'<span class="card-sub">{sheet_name}</span></a>')
        SEARCH_INDEX.append({"t": label, "c": "트래커", "u": f"tracker/{slug}.html"})
    print(f"  트래커: {len(cards)}개 시트 → tracker/")

    body = ('<h1>마스터 트래커</h1>'
            '<p class="meta">TP_Europe_Travel_Master_Tracker_v1.1.xlsx에서 변환</p>'
            f'<div class="grid">{"".join(cards)}</div>')
    (out_dir / "index.html").write_text(
        page("마스터 트래커", body, rel="..", topbar_title="마스터 트래커"),
        encoding="utf-8")


# ---------------------------------------------------------------- data.js

def build_data_js():
    CHAPTER_DATE_URL.update(DAY_OVERRIDES)
    today_map = {}
    d = TRIP_START
    while d <= TRIP_END:
        today_map[d.isoformat()] = f"daily/day-{day_no(d):02d}.html"
        d += timedelta(days=1)
    data = {
        "tripStart": TRIP_START.isoformat(),
        "tripEnd": TRIP_END.isoformat(),
        "today": today_map,
        "search": SEARCH_INDEX,
    }
    js = "window.GUIDE = " + json.dumps(data, ensure_ascii=False) + ";\n"
    (SITE / "assets" / "data.js").write_text(js, encoding="utf-8")
    print(f"  data.js: 날짜 매핑 {len(today_map)}일 · 검색 인덱스 {len(SEARCH_INDEX)}항목")


# ---------------------------------------------------------------- checks

def check_links():
    broken = []
    for f in SITE.rglob("*.html"):
        text = f.read_text(encoding="utf-8")
        for attr in ("href", "src"):
            for target in re.findall(rf'{attr}="([^"]+)"', text):
                if target.startswith(("http", "#", "mailto:", "data:")) or "${" in target:
                    continue
                path = (f.parent / target.split("#")[0]).resolve()
                if not path.exists():
                    broken.append(f"{f.relative_to(SITE)} → {target}")
    if broken:
        print("깨진 링크:")
        for b in broken:
            print("  " + b)
        sys.exit(1)
    print("링크 검사: 이상 없음")


def check_dates():
    d = TRIP_START
    missing = []
    while d <= TRIP_END:
        if d.isoformat() not in CHAPTER_DATE_URL:
            missing.append(d.isoformat())
        d += timedelta(days=1)
    if missing:
        print("챕터 날짜 매핑 누락:", ", ".join(missing))
        sys.exit(1)
    print(f"날짜 매핑 검사: {TRIP_START} ~ {TRIP_END} 전체 43일 이상 없음")


# ---------------------------------------------------------------- main

def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    (SITE / "assets").mkdir()
    shutil.copy(ASSETS / "style.css", SITE / "assets" / "style.css")
    shutil.copy(ASSETS / "nav.js", SITE / "assets" / "nav.js")

    print("챕터 빌드:")
    build_chapters()
    print("데일리 카드 빌드:")
    build_daily()
    build_home()
    print("지도 빌드:")
    build_maps()
    print("트래커 빌드:")
    build_tracker()
    build_data_js()
    check_links()
    check_dates()
    print(f"\n완료: {SITE} ({sum(1 for _ in SITE.rglob('*.html'))}개 HTML 페이지)")


if __name__ == "__main__":
    main()
