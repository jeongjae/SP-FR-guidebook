#!/usr/bin/env python3
"""콘텐츠 손실 감사 — 승격된 장문이 전부 렌더되는가.

KPI 는 content loss = 0 이다. 구조를 바꾸면서 글이 조용히 사라지는 것이
이 마이그레이션의 가장 큰 위험이라 기계로 확인한다.

원문과 렌더 결과를 **같은 방식으로** 납작하게 만든 뒤 비교한다. 한쪽만
괄호를 지우면 멀쩡한 문단이 사라진 것처럼 보인다 (실제로 그렇게 틀렸다).

    python3 build/content_audit.py [site_dir]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render import strip_tokens   # noqa: E402  렌더러와 같은 토큰 변환을 쓴다

ROOT = Path(__file__).resolve().parent.parent
PLACE_DIR = ROOT / "source" / "CURRENT" / "30_Places"

MIN_PARA = 40      # 이보다 짧은 조각은 표 셀·목록 머리라 비교 의미가 없다
PROBE = 45         # 문단 앞부분을 지문으로 쓴다


def flatten(text: str) -> str:
    """비교용 정규화. 원문과 렌더 결과에 똑같이 적용해야 한다."""
    # 토큰은 렌더러와 똑같이 바꾼다. 한쪽만 지우면 {{badge:x|재확인}} 이
    # 렌더에서는 "(재확인)" 이 되고 원문에서는 사라져 비교가 어긋난다.
    # 엔티티를 먼저 푼다. 나중에 풀면 &gt; 가 기호 제거를 피해 살아남아
    # 원문에는 없는 '>' 가 렌더 쪽에만 남는다.
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    text = strip_tokens(text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)  # 링크 → 글자만
    # 표 정렬행(|---|:--:|)은 원문에만 있다. 기호를 지운 뒤 처리하면
    # '------' 같은 찌꺼기가 남아 지문을 오염시킨다 — 먼저 줄째 지운다.
    text = re.sub(r"^[ \t]*\|?[\s|:-]*\|[\s|:-]*$", "", text, flags=re.M)
    text = re.sub(r"[*_`>#|~\[\]]", "", text)          # 마크다운 기호
    text = re.sub(r"^\s*[-:]{2,}\s*$", "", text, flags=re.M)
    # 목록 표시. 원문에만 남으면 멀쩡한 목록이 사라진 것처럼 보인다.
    text = re.sub(r"^\s*[-+•]\s+", "", text, flags=re.M)
    text = re.sub(r"^\s*\d+[.)]\s+", "", text, flags=re.M)
    return re.sub(r"\s+", "", text)


def page_text(html: str) -> str:
    html = re.sub(r"<script.*?</script>", "", html, flags=re.S)
    html = re.sub(r"<style.*?</style>", "", html, flags=re.S)
    return flatten(re.sub(r"<[^>]+>", " ", html))


def main() -> int:
    site = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "site"
    missing, checked, paras = [], 0, 0

    for src in sorted(PLACE_DIR.glob("*.md")):
        slug = src.stem
        page = site / "places" / f"{slug}.html"
        if not page.exists():
            missing.append((slug, "페이지 자체가 없다", 99))
            continue
        checked += 1
        body = re.sub(r"^---\n.*?\n---\n", "",
                      src.read_text(encoding="utf-8"), flags=re.S)
        rendered = page_text(page.read_text(encoding="utf-8"))
        miss, total = [], 0
        for para in re.split(r"\n\s*\n", body):
            flat = flatten(para)
            if len(flat) < MIN_PARA:
                continue
            total += 1
            paras += 1
            if flat[:PROBE] not in rendered:
                miss.append(para.strip()[:70])
        if miss:
            missing.append((slug, f"{len(miss)}/{total} 문단", len(miss)))

    print(f"장소 {checked}개 · 문단 {paras}개 검사")
    if missing:
        print(f"\n손실 {len(missing)}건:")
        for slug, why, _ in sorted(missing, key=lambda x: -x[2])[:20]:
            print(f"  {slug:42s} {why}")
        return 1
    print("콘텐츠 손실 0 — 승격된 장문이 전부 렌더된다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
