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
}

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


def regenerate(quiet: bool = True) -> dict[str, dict]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = {}
    for slug, fname in CHAPTER_FILES.items():
        path = CHAPTERS / fname
        if not path.exists():
            continue
        layers = extract(slug, path)
        result[slug] = layers
        parts = [f"---", f"slug: {slug}",
                 f"source: source/CURRENT/20_Regional_Chapters/{fname}", "---", ""]
        for key, _rx in LAYERS:
            if key in layers:
                parts += [f"## {LAYER_TITLE[key]}", "", layers[key], ""]
        (OUT_DIR / f"{slug}.md").write_text("\n".join(parts).rstrip() + "\n",
                                            encoding="utf-8")
    if not quiet:
        for slug, layers in result.items():
            got = " ".join(k for k, _ in LAYERS if k in layers)
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
