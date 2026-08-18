#!/usr/bin/env python3
"""콘텐츠 모델 — Trip · Region · Day · Place · Preparation.

이 파일이 사이트의 정본 계층이다. 페이지 렌더러는 여기서 나온 엔티티만
읽고, 마크다운을 정규식으로 긁지 않는다.

왜 새로 만들었나. 이전 파이프라인은 8개 챕터 마크다운을 h2 제목 키워드로
10개 카테고리에 분류하고, 장소 장문은 정규식으로 잘라낸 뒤 실패하면
**이미 빌드된 HTML 을 다시 파싱**해 발췌를 만들었다. 원고 제목을 한 글자
고치면 콘텐츠가 조용히 다른 페이지로 갔다. 그래서 사이트가 "마크다운을
웹으로 변환한 것"처럼 보였던 것이다 — 실제로 그랬기 때문이다.

정본 규칙은 셋이다.

    1 Place  = 1 canonical long-form guide
    Day      = 실행의 정본 (시간표 · 이동 · 예약 · Plan B)
    Region   = 탐색과 이해. Day 시간표를 복제하지 않는다.

데이터 출처:
    data/daily-cards/day-NN.json      하루 전체 — stops·legs·좌표·시각·피로도
    source/CURRENT/10_Core/itinerary.json   숙박 거점과 박수 (검증됨)
    source/CURRENT/10_Core/regions.json     지역 편집 정보
    source/ASSETS/91_Place_Registry_v1.0.md 장소 명부
    source/CURRENT/30_Places/<slug>.md      장소 장문 (정본)
    data/place-facts.json                   운영시간·요금·예약 (근거·TTL 포함)
    data/images/image-manifest.json         사진
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DAILY_CARDS = ROOT / "data" / "daily-cards"
ITINERARY = ROOT / "source" / "CURRENT" / "10_Core" / "itinerary.json"
REGIONS_JSON = ROOT / "source" / "CURRENT" / "10_Core" / "regions.json"
REGISTRY_MD = ROOT / "source" / "ASSETS" / "91_Place_Registry_v1.0.md"
PLACE_DIR = ROOT / "source" / "CURRENT" / "30_Places"
PLACE_FACTS = ROOT / "data" / "place-facts.json"
IMAGE_MANIFEST = ROOT / "data" / "images" / "image-manifest.json"

WEEKDAY_KO = "월화수목금토일"


def _d(iso: str) -> date:
    return date.fromisoformat(iso)


def date_label(d: date) -> str:
    """9/4 금 — 현장에서 읽는 형식. 연도는 붙이지 않는다, 한 해 안의 여행이다."""
    return f"{d.month}/{d.day} {WEEKDAY_KO[d.weekday()]}"


# ---------------------------------------------------------------- Place

@dataclass
class Fact:
    """검증된 사실 하나. 근거와 신뢰도를 반드시 함께 들고 다닌다.

    현장에서 틀린 정보는 없느니만 못하다. 그래서 값만 옮기지 않는다 —
    누가 말했는지(source)와 얼마나 믿을 만한지(confidence)가 붙어 다닌다.
    """
    key: str
    value: str
    confidence: str            # official | secondary | unverified | unreachable
    source: str | None = None
    verified_at: str | None = None
    blocked_reason: str | None = None

    @property
    def is_confirmed(self) -> bool:
        return self.confidence in ("official", "secondary") and bool(self.value)

    @property
    def needs_recheck(self) -> bool:
        """확정처럼 보이면 안 되는 값. 현장에서 이걸 믿고 움직이면 사고다."""
        return not self.is_confirmed


@dataclass
class Place:
    slug: str
    name: str
    region: str
    kind: str = "spot"          # spot | walk | node
    grade: str | None = None    # essential | priority | optional | ...
    grade_label: str | None = None
    pin: str | None = None
    wiki: str | None = None
    wiki_lang: str = "en"
    lat: float | None = None
    lng: float | None = None
    summary: str = ""           # 한 줄 — 카드에 쓴다
    why_go: str = ""            # Experience 층
    dont_miss: list[str] = field(default_factory=list)
    body_md: str = ""           # Deep Guide — 장문 정본
    practical_md: str = ""      # 원고가 들고 있던 실용 표 (facts 를 보완한다)
    facts: dict[str, Fact] = field(default_factory=dict)
    photo: dict | None = None
    days: list[int] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"places/{self.slug}.html"

    @property
    def has_deep_guide(self) -> bool:
        return len(self.body_md.strip()) > 0

    def fact(self, key: str) -> Fact | None:
        return self.facts.get(key)


# ---------------------------------------------------------------- Day

@dataclass
class Stop:
    id: str
    order: int
    start: str | None
    end: str | None
    name: str
    category: str               # culture | sight | food | hotel | transport | ...
    lat: float | None
    lng: float | None
    summary: str = ""
    menu: str | None = None
    reservation: str | None = None
    optional: bool = False
    place: Place | None = None  # 장소 페이지가 있는 stop 만 연결된다

    @property
    def time_label(self) -> str:
        if self.start and self.end:
            return self.start
        return self.start or ""


@dataclass
class Leg:
    frm: str
    to: str
    mode: str                   # walk | metro | bus | train | drive | flight
    duration: str | None = None
    distance: str | None = None
    line: str | None = None


@dataclass
class Day:
    n: int
    date: date
    city: str
    title: str
    region: str                 # 그날 밤 자는 지역 (정본)
    regions: list[str]          # 이동일이면 둘
    country: str                # es | fr | es-fr | none
    source_status: str
    start_time: str | None
    end_time: str | None
    total_duration: str | None
    total_distance: str | None
    fatigue: str | None
    hotel: dict
    stops: list[Stop] = field(default_factory=list)
    legs: list[Leg] = field(default_factory=list)
    transport: list[str] = field(default_factory=list)
    food: list[str] = field(default_factory=list)
    highlights: list[str] = field(default_factory=list)
    backup: str | None = None
    map: dict | None = None
    needs_review: list[str] = field(default_factory=list)
    bookings: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"daily/day-{self.n:02d}.html"

    @property
    def label(self) -> str:
        return f"Day {self.n}"

    @property
    def date_label(self) -> str:
        return date_label(self.date)

    @property
    def is_transfer(self) -> bool:
        """거점을 옮기는 날. 짐을 들고 움직이므로 화면이 달라야 한다."""
        return len(self.regions) > 1

    @property
    def route_label(self) -> str:
        """Nice → Aix-en-Provence. 이동일에 첫 화면에서 가장 먼저 읽는 줄."""
        return self.city

    @property
    def reserved_stops(self) -> list[Stop]:
        return [s for s in self.stops if s.reservation]

    @property
    def place_stops(self) -> list[Stop]:
        return [s for s in self.stops if s.place is not None]

    @property
    def is_authoritative(self) -> bool:
        return self.source_status == "authoritative"


# ---------------------------------------------------------------- Region

@dataclass
class Region:
    slug: str
    name: str
    name_ko: str
    country: str
    base: str                   # 실제 숙박 거점 (Girona 지역인데 Bàscara 에서 잔다)
    tagline: str
    dek: str
    intensity: str = ""
    budget: str = ""
    rain_plan: str = ""
    checkin: date = None
    checkout: date = None
    nights: int = 0
    days: list[Day] = field(default_factory=list)
    places: list[Place] = field(default_factory=list)
    hero: dict | None = None

    @property
    def url(self) -> str:
        return f"guide/{self.slug}.html"

    @property
    def date_range(self) -> str:
        return f"{self.checkin.month}/{self.checkin.day} — {self.checkout.month}/{self.checkout.day}"

    @property
    def day_range(self) -> str:
        if not self.days:
            return ""
        first, last = self.days[0].n, self.days[-1].n
        return f"Day {first}" if first == last else f"Day {first}–{last}"

    @property
    def essential_places(self) -> list[Place]:
        """Don't Miss. 등급이 '필수' 인 것만."""
        return [p for p in self.places if p.grade == "essential"]

    @property
    def food_places(self) -> list[Place]:
        return [p for p in self.places if p.kind == "spot" and p.grade == "food"]


# ---------------------------------------------------------------- Trip

@dataclass
class Trip:
    start: date
    end: date
    days: list[Day]
    regions: list[Region]
    places: dict[str, Place]

    @property
    def total_days(self) -> int:
        return len(self.days)

    def day(self, n: int) -> Day | None:
        return next((d for d in self.days if d.n == n), None)

    def region(self, slug: str) -> Region | None:
        return next((r for r in self.regions if r.slug == slug), None)

    def day_for_date(self, d: date) -> Day | None:
        return next((x for x in self.days if x.date == d), None)

    def status_on(self, today: date) -> str:
        """홈이 어떤 모드로 열릴지. pre | travel | post."""
        if today < self.start:
            return "pre"
        if today > self.end:
            return "post"
        return "travel"

    def days_until(self, today: date) -> int:
        return (self.start - today).days


# ================================================================ 로더

def load_registry() -> list[dict]:
    """91_Place_Registry_v1.0.md 를 읽는다. 이 MD 가 장소 명부의 정본이다.

    gen_place_registry.py 를 다시 돌리면 손편집이 날아간다 — 편집은 MD 를
    직접 고친다.
    """
    rows, region = [], None
    grade_map = {
        "필수": "essential", "우선 추천": "priority", "추천": "priority",
        "선택": "optional", "대안": "alternative", "제외": "excluded",
    }
    chapter_region = {
        "04": "barcelona", "05": "girona", "06": "nice", "07": "aix",
        "08": "luberon", "09": "avignon", "10": "lyon", "11": "paris",
    }
    for line in REGISTRY_MD.read_text(encoding="utf-8").splitlines():
        h = re.match(r"^##\s+([a-z]+)\s*\((\d+)\)", line)
        if h:
            region = chapter_region.get(h.group(2), h.group(1))
            continue
        m = re.match(r"^\|\s*`([a-z0-9-]+)`\s*\|(.*)$", line)
        if not m or region is None:
            continue
        cells = [c.strip() for c in m.group(2).split("|")]
        def cell(i):
            v = cells[i] if i < len(cells) else ""
            return None if v in ("", "—", "-") else v
        wiki = cell(6)
        lang = "en"
        if wiki and ":" in wiki and len(wiki.split(":", 1)[0]) <= 3:
            lang, wiki = wiki.split(":", 1)
        rows.append({
            "slug": m.group(1),
            "name": cell(0) or m.group(1),
            "kind": cell(1) or "spot",
            "grade_label": cell(2),
            "grade": grade_map.get(cell(2) or "", None),
            "pin": cell(3),
            "wiki": wiki,
            "wiki_lang": lang,
            "region": region,
        })
    return rows


def load_facts() -> dict[str, dict[str, Fact]]:
    if not PLACE_FACTS.exists():
        return {}
    raw = json.loads(PLACE_FACTS.read_text(encoding="utf-8"))
    out: dict[str, dict[str, Fact]] = {}
    for slug, place in raw.get("places", {}).items():
        facts = {}
        for key, f in (place.get("facts") or {}).items():
            facts[key] = Fact(
                key=key,
                value=f.get("value", ""),
                confidence=f.get("confidence", "unverified"),
                source=f.get("source"),
                verified_at=f.get("verified_at"),
                blocked_reason=f.get("blocked_reason"),
            )
        out[slug] = facts
    return out


def load_images() -> dict[str, dict]:
    """placeId → 이미지. 카탈로그에 없으면 사진 자리를 아예 만들지 않는다.

    라이선스·출처·저작자가 없는 이미지는 빌드가 거부한다. 이 사이트는
    gh-pages 로 공개 배포되므로 '개인 사용만 허용' 은 실제로 쓸 수 없다.
    """
    if not IMAGE_MANIFEST.exists():
        return {}
    raw = json.loads(IMAGE_MANIFEST.read_text(encoding="utf-8"))
    images = raw if isinstance(raw, list) else raw.get("images", [])
    by_place, heroes = {}, {}
    for img in images:
        pid = img.get("placeId")
        if pid and pid not in by_place:
            by_place[pid] = img
        if img.get("regionHero"):
            heroes.setdefault(img.get("region") or img.get("regionSlug"), img)
    by_place["__heroes__"] = heroes
    return by_place


PLACE_FM = re.compile(r"^---\n(.*?)\n---\n", re.S)


def load_place_bodies() -> dict[str, dict]:
    """source/CURRENT/30_Places/<slug>.md — 장소 장문의 정본.

    한 장소 = 한 파일이다. 챕터 원고에서 정규식으로 잘라내던 것을 정식
    데이터로 승격시킨 결과다 (build/promote_places.py 가 한 번 옮겼다).
    """
    out: dict[str, dict] = {}
    if not PLACE_DIR.exists():
        return out
    for path in sorted(PLACE_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        meta: dict = {}
        m = PLACE_FM.match(text)
        if m:
            for line in m.group(1).splitlines():
                if ":" not in line:
                    continue
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()
                if v.startswith("[") and v.endswith("]"):
                    inner = v[1:-1].strip()
                    meta[k] = [x.strip().strip('"') for x in inner.split(",")] if inner else []
                else:
                    meta[k] = v.strip('"')
            text = text[m.end():]
        # 본문을 세 층으로 가른다. 승격 스크립트가 '## 왜 가는가' ·
        # '## 더 깊이' · '## 실용' 로 써 두었다. 여기서 나누지 않으면
        # 렌더러가 층을 구분하지 못하고, 층을 구분하려다 절을 지우게 된다.
        layers = {"why_go": [], "deep": [], "practical": []}
        current = "deep"
        for line in text.strip().splitlines():
            head = re.match(r"^##\s+(왜 가는가|더 깊이|실용)\s*$", line)
            if head:
                current = {"왜 가는가": "why_go", "더 깊이": "deep",
                           "실용": "practical"}[head.group(1)]
                continue
            layers[current].append(line)
        meta["why_go"] = "\n".join(layers["why_go"]).strip()
        meta["practical_md"] = "\n".join(layers["practical"]).strip()
        meta["body"] = "\n".join(layers["deep"]).strip()
        out[path.stem] = meta
    return out


def load_days(regions_by_slug: dict[str, dict], stays: list[dict]) -> list[Day]:
    """data/daily-cards/day-NN.json 43개. 하루의 정본이다.

    이 파일들에는 stops(좌표·시각·카테고리·예약)·legs·피로도·교통·식사·
    하이라이트·Plan B 가 전부 들어 있다. 예전 빌드는 이걸 두고 마크다운
    표를 정규식으로 다시 긁었다 — 그래서 원고와 화면이 갈릴 수 있었다.
    """
    days: list[Day] = []
    for path in sorted(DAILY_CARDS.glob("day-*.json")):
        j = json.loads(path.read_text(encoding="utf-8"))
        d = _d(j["date"])
        here = [s for s in stays if _d(s["checkin"]) <= d <= _d(s["checkout"])]
        sleeping = [s for s in here if _d(s["checkin"]) <= d < _d(s["checkout"])]
        primary = (sleeping or here)[-1]["key"] if (sleeping or here) else "return"
        slugs = [s["key"] for s in here] or ["return"]
        countries = {regions_by_slug.get(s, {}).get("country", "") for s in slugs}
        countries.discard("")
        country = "-".join(sorted(countries)) if len(countries) > 1 else \
            (next(iter(countries)) if countries else "none")

        days.append(Day(
            n=j["day"],
            date=d,
            city=j["city"],
            title=j["title"],
            region=primary,
            regions=slugs,
            country=country,
            source_status=j.get("sourceStatus", "prototype-reviewed"),
            start_time=j.get("startTime"),
            end_time=j.get("endTime"),
            total_duration=j.get("totalDuration"),
            total_distance=j.get("totalDistance"),
            fatigue=j.get("fatigue"),
            hotel=j.get("hotel") or {},
            stops=[Stop(
                id=s["id"], order=s["order"], start=s.get("start"), end=s.get("end"),
                name=s["name"], category=s.get("category", "sight"),
                lat=s.get("lat"), lng=s.get("lng"), summary=s.get("summary") or "",
                menu=s.get("menu"), reservation=s.get("reservation"),
                optional=bool(s.get("optional")),
            ) for s in j.get("stops", [])],
            legs=[Leg(
                frm=l["from"], to=l["to"], mode=l.get("mode", "walk"),
                duration=l.get("duration"), distance=l.get("distance"),
                line=l.get("line"),
            ) for l in j.get("legs", [])],
            transport=j.get("transport") or [],
            food=j.get("food") or [],
            highlights=j.get("highlights") or [],
            backup=j.get("backup"),
            map=j.get("map"),
            needs_review=j.get("needsReview") or [],
        ))
    return sorted(days, key=lambda x: x.n)


def load_trip() -> Trip:
    itin = json.loads(ITINERARY.read_text(encoding="utf-8"))
    stays = itin["stays"]
    regions_raw = json.loads(REGIONS_JSON.read_text(encoding="utf-8"))["regions"]
    by_slug = {r["slug"]: r for r in regions_raw}

    days = load_days(by_slug, stays)

    # --- 장소 조립: 명부 + 장문 + 사실 + 사진 -----------------------------
    facts = load_facts()
    images = load_images()
    heroes = images.pop("__heroes__", {})
    bodies = load_place_bodies()

    places: dict[str, Place] = {}
    for row in load_registry():
        body = bodies.get(row["slug"], {})
        places[row["slug"]] = Place(
            slug=row["slug"], name=row["name"], region=row["region"],
            kind=row["kind"], grade=row["grade"], grade_label=row["grade_label"],
            pin=row["pin"], wiki=row["wiki"], wiki_lang=row["wiki_lang"],
            summary=body.get("summary", ""),
            why_go=body.get("why_go", ""),
            dont_miss=body.get("dont_miss", []) or [],
            body_md=body.get("body", ""),
            practical_md=body.get("practical_md", ""),
            facts=facts.get(row["slug"], {}),
            photo=images.get(row["slug"]),
        )

    # --- Day ↔ Place: stop.id 로 직접 잇는다 ------------------------------
    # 예전에는 장소 이름을 시간표 문자열에 부분일치시키는 3단 휴리스틱이었다.
    # (Arles 가 Saint-Charles 에 매칭된 흔적이 주석에 남아 있었다.)
    # 이제 daily-cards 의 stop.id 가 곧 슬러그라 추측이 필요 없다.
    for d in days:
        for s in d.stops:
            p = places.get(s.id)
            if p is not None:
                s.place = p
                if d.n not in p.days:
                    p.days.append(d.n)
            # 좌표는 daily-card 가 더 최신이다 — 장소에 없으면 채워 준다
            if p is not None and p.lat is None and s.lat:
                p.lat, p.lng = s.lat, s.lng

    # --- 지역 조립 --------------------------------------------------------
    stay_by_key = {s["key"]: s for s in stays}
    regions: list[Region] = []
    for r in regions_raw:
        stay = stay_by_key.get(r["slug"])
        if stay is None:
            continue
        regions.append(Region(
            slug=r["slug"], name=r["name"], name_ko=r.get("nameKo", r["name"]),
            country=r["country"], base=stay["base"],
            tagline=r.get("tagline", ""), dek=r.get("dek", ""),
            intensity=r.get("intensity", ""), budget=r.get("budget", ""),
            rain_plan=r.get("rainPlan", ""),
            checkin=_d(stay["checkin"]), checkout=_d(stay["checkout"]),
            nights=stay["nights"],
            days=[d for d in days if r["slug"] in d.regions],
            places=[p for p in places.values() if p.region == r["slug"]],
            hero=heroes.get(r["slug"]),
        ))

    return Trip(
        start=_d(itin["trip"]["start"]),
        end=_d(itin["trip"]["end"]),
        days=days, regions=regions, places=places,
    )


# ================================================================ 검증

def validate(trip: Trip) -> list[str]:
    """구조 무결성. 여기서 걸리면 빌드를 세운다.

    현장에서 깨진 링크나 빠진 하루를 만나는 것이 최악이다.
    """
    problems = []

    if len(trip.days) != 43:
        problems.append(f"Day 가 43일이 아니다: {len(trip.days)}일")
    missing = [n for n in range(1, 44) if trip.day(n) is None]
    if missing:
        problems.append(f"빠진 Day: {missing}")

    if len(trip.regions) != 8:
        problems.append(f"지역이 8개가 아니다: {len(trip.regions)}개")

    # 날짜 연속성 — 하루라도 건너뛰면 일정이 어긋난 것이다
    for a, b in zip(trip.days, trip.days[1:]):
        if b.date - a.date != timedelta(days=1):
            problems.append(f"날짜 불연속: Day {a.n} {a.date} → Day {b.n} {b.date}")

    # 고아 장소 — 어느 지역에도 속하지 않으면 길이 끊긴다
    region_slugs = {r.slug for r in trip.regions}
    for p in trip.places.values():
        if p.region not in region_slugs:
            problems.append(f"고아 장소: {p.slug} (region={p.region})")

    # leg 의 양끝은 그날의 stop 이어야 한다
    for d in trip.days:
        ids = {s.id for s in d.stops}
        for l in d.legs:
            if l.frm not in ids or l.to not in ids:
                problems.append(f"Day {d.n}: leg {l.frm}→{l.to} 가 stop 을 벗어난다")

    return problems


if __name__ == "__main__":
    import sys
    trip = load_trip()
    problems = validate(trip)
    print(f"Trip {trip.start}–{trip.end} · {trip.total_days}일 · 지역 {len(trip.regions)}개")
    print(f"장소 {len(trip.places)}개 · 장문 보유 "
          f"{sum(1 for p in trip.places.values() if p.has_deep_guide)}개")
    linked = sum(len(d.place_stops) for d in trip.days)
    print(f"Day↔Place 연결 {linked}건 · stop 총 {sum(len(d.stops) for d in trip.days)}건")
    for r in trip.regions:
        print(f"  {r.slug:10s} {r.day_range:12s} {r.nights}박 "
              f"장소 {len(r.places):3d} 필수 {len(r.essential_places)}")
    if problems:
        print(f"\n검증 실패 {len(problems)}건:")
        for p in problems:
            print("  " + p)
        sys.exit(1)
    print("\n검증 통과")
