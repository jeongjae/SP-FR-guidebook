#!/usr/bin/env python3
"""빈 줄 없이 이어 붙은 표가 열을 잃는지 전 원고에서 검사한다.

    python3 build/table_loss_check.py

마크다운은 표 하나에 구분선(`|---|---|`) 하나를 기대한다. 원고가 표 두세
개를 줄바꿈 하나로 붙여 놓으면 **표 하나**로 읽고, 첫 표의 열 수에 맞춰 뒤
표의 열을 잘라 버린다. 잘린 열은 화면에도, 검색에도, 오프라인 저장본에도
없다. 열 수가 일정하게 잘리기 때문에 기존 표 검사(ux_check)도 못 잡는다.

Barcelona '한눈에 보기' 가 그랬다 — `확정 일정`·`예상 체류`·`핵심 이유`
세 열이 통째로 사라져 있었다.

`render.split_stacked_tables` 가 덩어리를 갈라 놓는다. 이 검사는 **고치기
전이었다면 몇 열을 잃었을지**를 세어, 같은 패턴이 어디에 더 있는지 보여
주고, 수정 뒤에 손실이 0 인지 확인한다.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import render  # noqa: E402
from render import SEP_ROW, split_stacked_tables  # noqa: E402

CORPUS = [
    ROOT / "source" / "CURRENT" / "20_Regional_Chapters",
    ROOT / "source" / "CURRENT" / "20_Regions",
    ROOT / "source" / "CURRENT" / "30_Places",
    ROOT / "source" / "CURRENT" / "10_Core",
    ROOT / "source" / "ASSETS",
]


def cells(line: str) -> int:
    return len([c for c in line.strip().strip("|").split("|")])


def stacked_blocks(text: str) -> list[dict]:
    """구분선이 둘 이상인 파이프 덩어리 = 붙어 있는 표."""
    out, block, start = [], [], 0
    lines = text.splitlines()

    def flush(end: int):
        if not block:
            return
        seps = [i for i, ln in enumerate(block) if SEP_ROW.match(ln)]
        if len(seps) > 1:
            widths = []
            for i in seps:
                head = block[i - 1] if i else block[i]
                widths.append(cells(head))
            # 첫 표의 열 수로 잘리므로, 그보다 넓은 표의 초과분이 손실이다
            lost = sum(max(0, w - widths[0]) for w in widths[1:])
            out.append({"line": start + 1, "tables": len(seps),
                        "widths": widths, "lost_columns": lost})
        block.clear()

    for i, line in enumerate(lines):
        if line.lstrip().startswith("|"):
            if not block:
                start = i
            block.append(line)
            continue
        flush(i)
    flush(len(lines))
    return out


def scan() -> tuple[list[dict], int]:
    findings, lost = [], 0
    for root in CORPUS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            text = path.read_text(encoding="utf-8")
            for block in stacked_blocks(text):
                rel = str(path.relative_to(ROOT)).replace("\\", "/")
                findings.append({**block, "file": rel})
                lost += block["lost_columns"]
    return findings, lost


def residual() -> list[str]:
    """수정을 적용한 뒤에도 덩어리가 남는가. 남으면 0 이 아니다."""
    problems = []
    for root in CORPUS:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md")):
            fixed = split_stacked_tables(path.read_text(encoding="utf-8"))
            for block in stacked_blocks(fixed):
                rel = str(path.relative_to(ROOT)).replace("\\", "/")
                problems.append(f"{rel}:{block['line']} — 표 {block['tables']}개가 "
                                f"아직 붙어 있다 (열 {block['widths']})")
    return problems


def main() -> int:
    findings, lost = scan()
    print("연속 표 병합 검사 — 원고 전수")
    print(f"  붙어 있는 표 덩어리      {len(findings)}")
    print(f"  수정 전이면 잃었을 열     {lost}")
    by_file: dict[str, int] = {}
    for f in findings:
        by_file[f["file"]] = by_file.get(f["file"], 0) + f["lost_columns"]
    for name, n in sorted(by_file.items(), key=lambda x: -x[1]):
        mark = "  ← 열 손실" if n else ""
        print(f"    {name}  {n}{mark}")

    problems = residual()
    if problems:
        print(f"\n수정 후에도 남은 덩어리 {len(problems)}건:")
        for p in problems[:20]:
            print("  " + p)
        return 1
    print("\n수정 후 남은 병합 0 — 조용한 열 손실 없음")
    return 0


if __name__ == "__main__":
    sys.exit(main())
