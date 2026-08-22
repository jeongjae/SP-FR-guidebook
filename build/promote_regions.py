#!/usr/bin/env python3
"""지역 편집 섹션을 챕터 원고에서 정식 데이터로 승격시킨다.

    source/CURRENT/20_Regional_Chapters/*.md
        ↓  빌드마다 다시 뽑는다
    source/CURRENT/20_Regions/<slug>.md

장소(30_Places)와 같은 구조다. 왜 필요했나 — 새 지역 페이지를 데이터로만
짓다 보니 원고의 편집 판단이 통째로 빠졌다. Editor's Verdict(이 지역에
시간을 쓸 가치와 한계) · 꼭 경험할 세 장면 · 생략해도 되는 것 · 한눈에
보기가 화면에서 사라진 것을 콘텐츠 스키마 가드가 잡았다.

이 네 가지가 "이 지역에서 무엇을 볼 가치가 있는가" 라는 Region 의 질문에
직접 답하는 부분이라 빠지면 지역 페이지가 목록만 남는다.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "source" / "CURRENT" / "20_Regional_Chapters"
OUT_DIR = ROOT / "source" / "CURRENT" / "20_Regions"

CHAPTER_FILES = {
    "barcelona": "04_Barcelona_Sitges_v2.0.md",
    "girona": "05_Girona_Collioure_Emporda_v2.1.md",
    "nice": "06_Nice_Cote_d_Azur_v2.0.md",
    "aix": "07_Aix_en_Provence_v2.0.md",
    "luberon": "08_Luberon_Farmhouse_v2.0.md",
    "avignon": "09_Avignon_Alpilles_Pont_du_Gard_v2.0.md",
    "lyon": "10_Lyon_v2.0.md",
    "paris": "11_Paris_Long_Stay_v2.0.md",
}

# 원고 h2 → 지역 페이지의 층. 앞의 것이 먼저 맞는다.
LAYERS = [
    ("verdict",   re.compile(r"^Editor.s Verdict")),
    ("scenes",    re.compile(r"^꼭 경험할 세 장면")),
    ("skip",      re.compile(r"^생략해도 되는 것")),
    ("overview",  re.compile(r"^한눈에 보기")),
    ("role",      re.compile(r"^여행 전체에서의 역할|^이 체류의 역할")),
    ("rhythm",    re.compile(r"^추천 체류 리듬")),
]
LAYER_TITLE = {
    "verdict": "이 지역에 시간을 쓸 가치와 한계",
    "scenes": "꼭 경험할 세 장면",
    "skip": "생략해도 되는 것",
    "overview": "한눈에 보기",
    "role": "여행 전체에서의 역할",
    "rhythm": "추천 체류 리듬",
    "neighborhoods": "숙소 생활권과 동네",
    "transport_deep": "지역 교통 심화",
    "food_culture": "음식·시장·카페·생활체험",
}

# --- 심화 층 (FCR-02) ------------------------------------------------------
# 위의 여섯 층은 h2 하나와 그 아래 절만 가져온다. 아래 세 층은 다르다 —
# 원고가 하위 주제에도 h2 를 쓰기 때문에 "다음 h2" 로 끊으면 첫 문단만
# 가져오고 나머지를 버린다. 그래서 **스키마가 정한 척추 제목**까지를
# 한 덩어리로 본다.
#
# 왜 필요했나. 숙소 생활권·도착출발·음식시장 세 덩어리가 원고에만 있고
# 사이트 어디에도 없었다. 'Barcelona 카페 5곳'·'슈퍼마켓 사용 원칙'·
# '저배출구역' 을 배포본에서 찾으면 하나도 안 나온다. 지역 페이지에
# Accommodation·Local Life·Transport 를 세우려면 이 원고가 있어야 한다.
SPINE = [
    "Editor’s Verdict", "꼭 경험할 세 장면", "생략해도 되는 것", "한눈에 보기",
    "여행 전체에서의 역할", "추천 체류 리듬", "구역별 이해와 숙소 생활권",
    "지역을 이해하는 다섯 개의 층", "도착·출발·지역 내 교통", "핵심 셀프가이드",
    "음식·시장·카페·생활체험", "당일치기·우천·피로 대안", "예약·비용·안전·주차·귀가",
    "공식 확인 정보와 재확인 대상", "검증 상태", "실행지도 · 현장 사용",
]

# 원고는 이 덩어리들을 h2 로도 h3 로도 쓴다. Barcelona 는 '동네별 성격과
# 숙소 적합성' 이 '지역을 이해하는 다섯 개의 층' 아래 h3 로 들어가 있고,
# Girona 는 같은 내용이 h2 '구역별 이해와 숙소 생활권' 바로 아래에 있다.
# 그래서 층은 **제목 이름**으로 잡고, 덩어리는 다음 경계 제목까지로 끊는다.
DEEP_LAYERS = [
    ("context", ["지역을 이해하는 다섯 개의 층"]),
    ("neighborhoods", ["구역별 이해와 숙소 생활권", "동네별 성격과 숙소 적합성"]),
    ("stay_budget", ["숙소 예산과 확정 숙소"]),
    ("transport_deep", ["도착·출발·지역 내 교통"]),
    ("food_culture", ["음식·시장·카페·생활체험"]),
]

# 층이 서로를 삼키지 않게 막는 경계. h1 · 척추 h2 · 위의 하위 앵커.
SUB_ANCHORS = [a for _, anchors in DEEP_LAYERS for a in anchors]

# 폐기된 숙소 후보. 확정 숙소가 있는 지역에서는 화면에 올리지 않는다 —
# 후보 주소를 확정으로 믿고 이동하는 것이 이 프로젝트 최악의 사고다.
# 동네 순위('7.1 Dreta de l’Eixample 동부 — 가장 균형 잡힌 1순위')는 남긴다.
# 그건 '어디에 묵을 만한가' 라는 Accommodation 의 답이고, 숙소 후보는
# 이미 예약이 끝난 자리의 옛 비교표다.
STAY_CANDIDATE = re.compile(
    r"^(?:\d+(?:\.\d+)?\s+)?\d+\s*순위\s*[:：—–-]|후보|숙소 선택 결론")

# 후보 걸러내기는 숙소 두 층에서만 한다. '13.6 추가 식당 후보'·'카페·빵집
# 후보' 는 음식 층의 정상 콘텐츠다.
STAY_LAYERS = {"neighborhoods", "stay_budget"}

HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_tidy import tidy  # noqa: E402


def sections(text: str):
    out, cur, fence = [], None, False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            fence = not fence
        m = None if fence else HEADING.match(line)
        if m:
            if cur:
                out.append(cur)
            cur = {"level": len(m.group(1)), "title": m.group(2), "lines": []}
        elif cur:
            cur["lines"].append(line)
    if cur:
        out.append(cur)
    return out


def extract(slug: str, path: Path) -> dict:
    secs = sections(path.read_text(encoding="utf-8"))
    found: dict[str, list[str]] = {}
    for i, sec in enumerate(secs):
        if sec["level"] != 2:
            continue
        key = next((k for k, rx in LAYERS if rx.match(sec["title"])), None)
        if key is None or key in found:
            continue
        body = ["\n".join(sec["lines"])]
        # 하위 절도 함께 가져온다 — 표와 목록이 거기 있다
        for nxt in secs[i + 1:]:
            if nxt["level"] <= 2:
                break
            body.append(f"{'#' * min(nxt['level'], 4)} {nxt['title']}")
            body.append("\n".join(nxt["lines"]))
        found[key] = [tidy("\n".join(body))]
    return {k: v[0] for k, v in found.items() if v[0].strip()}


def _is_boundary(sec: dict) -> bool:
    """층과 층 사이의 벽. 여기서 덩어리를 끊는다."""
    title = sec["title"]
    if sec["level"] == 1:
        return True
    if sec["level"] == 2 and any(title.startswith(s) for s in SPINE):
        return True
    return any(title.startswith(a) for a in SUB_ANCHORS)


LAYER_TITLE_EXTRA = {
    "context": "이 지역을 이해하는 층",
    "stay_budget": "숙소 예산과 확인 기준",
}


def extract_deep(secs: list[dict], drop_stay_candidates: bool) -> dict:
    """앵커 제목에서 다음 경계 제목까지를 통째로 가져온다.

    하위 제목은 한 단계씩 내린다. 안 내리면 절 제목이 지역 페이지의 섹션
    제목과 같은 크기로 나와 여섯 섹션 구조가 무너진다.
    """
    out: dict[str, str] = {}
    bounds = [i for i, sec in enumerate(secs) if _is_boundary(sec)]
    for key, anchors in DEEP_LAYERS:
        chunks = []
        for anchor in anchors:
            begin = next((i for i, sec in enumerate(secs)
                          if sec["title"].startswith(anchor)), None)
            if begin is None:
                continue
            end = next((i for i in bounds if i > begin), len(secs))
            base = secs[begin]["level"]
            drop = drop_stay_candidates and key in STAY_LAYERS
            body, skip_level = ["\n".join(secs[begin]["lines"])], None
            for sec in secs[begin + 1:end]:
                if skip_level is not None:
                    if sec["level"] > skip_level:
                        continue
                    skip_level = None
                if drop and STAY_CANDIDATE.search(sec["title"]):
                    skip_level = sec["level"]
                    continue
                level = min(max(sec["level"] - base + 3, 3), 5)
                body.append(f"{'#' * level} {sec['title']}")
                body.append("\n".join(sec["lines"]))
            chunk = tidy("\n".join(body))
            if chunk.strip():
                chunks.append(chunk)
        if chunks:
            out[key] = "\n\n".join(chunks)
    return out


def confirmed_stay_regions() -> set[str]:
    """숙소가 확정된 지역. 확정된 곳에서는 옛 후보 목록을 올리지 않는다."""
    import json
    cards = ROOT / "data" / "daily-cards"
    itin = json.loads((ROOT / "source" / "CURRENT" / "10_Core" / "itinerary.json")
                      .read_text(encoding="utf-8"))
    stays = {s["key"]: (s["checkin"], s["checkout"]) for s in itin["stays"]}
    confirmed = set()
    for path in sorted(cards.glob("day-*.json")):
        j = json.loads(path.read_text(encoding="utf-8"))
        hotel = j.get("hotel") or {}
        if hotel.get("status") != "confirmed":
            continue
        for slug, (a, b) in stays.items():
            if a <= j["date"] < b:
                confirmed.add(slug)
    return confirmed


def regenerate(quiet: bool = True) -> dict[str, dict]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    confirmed = confirmed_stay_regions()
    result = {}
    for slug, fname in CHAPTER_FILES.items():
        path = CHAPTERS / fname
        if not path.exists():
            continue
        layers = extract(slug, path)
        secs = sections(path.read_text(encoding="utf-8"))
        layers.update(extract_deep(secs, drop_stay_candidates=slug in confirmed))
        result_titles = {**LAYER_TITLE, **LAYER_TITLE_EXTRA}
        result[slug] = layers
        parts = [f"---", f"slug: {slug}",
                 f"source: source/CURRENT/20_Regional_Chapters/{fname}", "---", ""]
        order = [k for k, _ in LAYERS] + [k for k, _ in DEEP_LAYERS]
        for key in order:
            if key in layers:
                parts += [f"## {result_titles[key]}", "", layers[key], ""]
        (OUT_DIR / f"{slug}.md").write_text("\n".join(parts).rstrip() + "\n",
                                            encoding="utf-8")
    if not quiet:
        for slug, layers in result.items():
            got = " ".join(k for k in
                           [x for x, _ in LAYERS] + [x for x, _ in DEEP_LAYERS]
                           if k in layers)
            print(f"  {slug:10s} {got}")
    return result


def main() -> int:
    result = regenerate(quiet=False)
    missing = {s: [k for k, _ in LAYERS[:4] if k not in v] for s, v in result.items()}
    missing = {s: m for s, m in missing.items() if m}
    print(f"\n지역 {len(result)}개 승격 → {OUT_DIR.relative_to(ROOT)}")
    if missing:
        print("핵심 층 누락:")
        for s, m in missing.items():
            print(f"  {s}: {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
