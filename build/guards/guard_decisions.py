#!/usr/bin/env python3
"""G5 — Jason 확정 결정의 forbidden_patterns 잔존 검출.

decisions.json 이 정본이다. 결정이 뒤집히면 원고가 아니라 그 파일을 먼저 고친다.
"""
import fnmatch
import sys

from common import chapter_files, decisions, report


def main():
    problems = []
    for d in decisions():
        pats = d.get("forbidden_patterns") or []
        scopes = d.get("scope") or ["*"]
        if not pats:
            continue
        for f in chapter_files():
            if not any(fnmatch.fnmatch(f.name, s) for s in scopes):
                continue
            for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                for pat in pats:
                    if pat in line:
                        problems.append(
                            f"{d['id']} {f.name}:{i} '{pat}' — {d['decision'][:34]}")
    return report("G5", "확정 결정 잔재", problems)


if __name__ == "__main__":
    sys.exit(main())
