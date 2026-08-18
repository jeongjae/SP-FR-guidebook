#!/usr/bin/env python3
"""마크다운 위생 — 승격할 때마다 똑같이 적용된다.

원고는 사람이 쓴 것이라 표 앞뒤에 빈 줄이 없는 곳이 많다. 마크다운은 그
빈 줄로 블록을 가르기 때문에, 없으면 표 바로 뒤 문장이 **표의 한 행으로
빨려 들어간다.** 그러면 한 칸짜리 행이 생겨 열 너비가 문장 길이만큼
늘어나고 표가 읽을 수 없게 된다. Nice 의 '시간을 쓸 가치와 한계' 가
그랬다 — 긴 산문 한 문단이 '항목' 열에 들어가 있었다.

여기서 고치는 것은 형식뿐이다. 글자는 건드리지 않는다.
"""
from __future__ import annotations

import re

LAYER_HEADS = ("왜 가는가", "더 깊이", "실용")

# |---|---| 같은 표 구분선
SEP_ROW = re.compile(r"^\s*\|?[\s:|-]*-{2,}[\s:|-]*\|?\s*$")


def _is_row(line: str) -> bool:
    return line.lstrip().startswith("|")


def tidy(md_text: str, *, normalize_headings: bool = False) -> str:
    """표·인용 블록을 빈 줄로 가르고, 필요하면 헤딩 레벨을 맞춘다.

    normalize_headings 는 장소 파일에서만 켠다. 거기서는 '왜 가는가 / 더 깊이
    / 실용' 이 뼈대이고 그 아래는 전부 같은 층이라 h3 으로 통일한다.
    """
    out: list[str] = []
    fence = False
    lines = md_text.splitlines()

    for i, line in enumerate(lines):
        if line.strip().startswith("```"):
            fence = not fence
            out.append(line)
            continue
        if fence:
            out.append(line)
            continue

        prev = out[-1] if out else ""
        nxt = lines[i + 1] if i + 1 < len(lines) else ""

        # 표가 시작되는데 앞 줄이 다른 글이면 빈 줄을 넣는다.
        # 없으면 마크다운이 앞 문단의 일부로 읽어 표가 아예 안 만들어진다.
        if _is_row(line) and prev.strip() and not _is_row(prev):
            out.append("")

        # 인용문이 표에 붙어 있으면 '>' 가 글자로 출력된다.
        if line.lstrip().startswith(">") and prev.strip().startswith("|"):
            out.append("")

        if normalize_headings:
            m = re.match(r"^(#{3,6})\s+(.*)$", line)
            if m and m.group(2).strip() not in LAYER_HEADS:
                line = "### " + m.group(2).strip()

        out.append(line)

        # 표가 끝나는데 다음 줄이 바로 다른 글이면 빈 줄을 넣는다.
        # 이게 없으면 그 줄이 표의 한 행이 되어 열 너비를 망가뜨린다.
        if _is_row(line) and nxt.strip() and not _is_row(nxt):
            out.append("")

    # 빈 줄이 셋 이상 이어지면 둘로 줄인다
    text = "\n".join(out)
    return re.sub(r"\n{3,}", "\n\n", text).strip()
