#!/usr/bin/env python3
"""원고 흔적 가드 — 제작과정의 자국이 독자 화면에 새지 않는가.

    python3 build/manuscript_residue_check.py

챕터 원고를 지역 페이지로 승격시키는 파이프라인이 있다
(`promote_regions.py`). 편한 대신 위험하다 — 원고의 절 번호(`13.2`),
편집용 제목(`… — 원고`), 내부 모듈 이름(`Commercial Guide Module`),
앞뒤 문맥을 잃은 조각(`아래 실행표 기준 준수`)이 **그대로 렌더된다.**
실제로 Barcelona 지역 페이지에는 절 번호 헤딩이 37개 있었다.

이건 사실이 틀린 것도 링크가 깨진 것도 아니라서 다른 가드가 잡지 못한다.
그런데 현장에서는 "5.3절" 이라는 말이 가리키는 절이 어디에도 없다.

**렌더된 HTML 의 보이는 글자만 본다.** 원고에는 절 번호가 남아 있어도
된다 — 원고는 원고다. 문제는 그것이 독자 화면에 나올 때다.

통폐합이 끝난 지역만 강제한다(`data/region-consolidation.json`). 아직인
지역은 세어서 보여 준다. 지역마다 따로 정리하기 때문이고, 끝난 지역이
되돌아가는 것만 막으면 된다.
"""
from __future__ import annotations

import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = Path(os.environ.get("SPFR_SITE_DIR") or (ROOT / "site"))
CONSOLIDATION = ROOT / "data" / "region-consolidation.json"

# 흔적의 종류. 기계적으로 문자열을 지우라는 뜻이 아니라, 사람이 의미를
# 보고 다시 쓰라는 신호다.
PATTERNS: list[tuple[str, re.Pattern]] = [
    ("원고 편집용 제목", re.compile(r"[—–-]{1,2}\s*원고\s*$|[—–-]{1,2}\s*원고\s*[<|]")),
    ("원고 절 번호 헤딩", re.compile(r"^\d+\.\d+(\.\d+)?\s+\S")),
    ("내부 모듈 이름", re.compile(r"Commercial Guide Module|"
                            r"Regional Context & Scheduled Place Dossiers")),
    ("제작 단계 표현", re.compile(r"\bResearch Pass\b|\bLayer\s*\d|\bPhase\s*\d")),
    ("원본 문서 구조", re.compile(r"\bSection\s+\d|\bChapter\s+\d")),
    ("초안 표기", re.compile(r"(?<![가-힣])초안(?![가-힣])|\bdraft\b", re.I)),
    ("소스 경로", re.compile(r"source/(?:CURRENT|ARCHIVE)/|data/[a-z-]+\.json|"
                         r"\b\d\d_[A-Za-z_]+\.md\b")),
    ("문맥 없는 조각", re.compile(
        r"앞서 본 것처럼|후자의 경우|위의 후보 (?:가운데|중)|앞의 표 기준|"
        r"위 표 참조|아래 실행표|다음 장에서|본 원고|앞의 \d+\.\d+")),
]


def visible_lines(path: Path) -> list[str]:
    """보이는 글자만. 스크립트·스타일·SVG·속성값은 화면이 아니다."""
    s = path.read_text(encoding="utf-8")
    for pat in (r"<script.*?</script>", r"<style.*?</style>", r"<svg.*?</svg>"):
        s = re.sub(pat, "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "\n", s)
    return [ln.strip() for ln in html.unescape(s).splitlines() if ln.strip()]


def scan(slug: str) -> list[tuple[str, str]]:
    path = SITE / "guide" / f"{slug}.html"
    if not path.exists():
        return []
    hits = []
    for line in visible_lines(path):
        for label, rx in PATTERNS:
            if rx.search(line):
                hits.append((label, line[:90]))
    return hits


def main() -> int:
    conf = json.loads(CONSOLIDATION.read_text(encoding="utf-8"))
    strict = set(conf.get("consolidated") or [])
    slugs = sorted(p.stem for p in (SITE / "guide").glob("*.html")
                   if p.stem != "index")
    failures, pending = [], {}
    for slug in slugs:
        hits = scan(slug)
        if slug in strict:
            failures += [(slug, label, line) for label, line in hits]
        elif hits:
            pending[slug] = len(hits)

    if failures:
        print(f"원고 흔적 가드: 통폐합 완료 지역에서 {len(failures)}건")
        for slug, label, line in failures[:40]:
            print(f"  {slug} · {label} — {line}")
        if len(failures) > 40:
            print(f"  … 그 밖에 {len(failures) - 40}건")
        return 1

    done = ", ".join(sorted(strict)) or "없음"
    print(f"원고 흔적 가드: 통폐합 완료 {done} — 흔적 0")
    if pending:
        rest = " · ".join(f"{s} {n}" for s, n in sorted(pending.items()))
        print(f"  아직 통폐합하지 않은 지역 (세기만 한다): {rest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
