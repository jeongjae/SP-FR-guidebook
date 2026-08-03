#!/usr/bin/env python3
"""콘텐츠 감사 도구 — 인벤토리·중복 탐지·제목 감사.

읽기 전용이다. source/ 의 마크다운과 site/ 의 HTML 을 훑고
data/ 아래 CSV 와 docs/ 보고서용 통계를 만든다. 어떤 원고도 수정하지 않는다.

사용:
    python3 build/audit_content.py

출력:
    data/content-inventory.csv          섹션 단위 인벤토리
    data/content-duplicate-matrix.csv   중복 그룹 (exact + near)
    data/content-boilerplate.csv        3개 파일 이상 반복되는 문장
    data/audit-stats.json               보고서용 집계
"""
from __future__ import annotations

import csv
import difflib
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
SITE = ROOT / "site"
DATA = ROOT / "data"

# ---------------------------------------------------------------- 정규화

MD_SYM = re.compile(r"[*_`>#|:\-—–·•]+")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
IMG = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
BADGE = re.compile(r"\{\{[^}]*\}\}")
WS = re.compile(r"\s+")


def normalize(text: str) -> str:
    text = IMG.sub(r"\1", text)
    text = LINK.sub(r"\1", text)
    text = BADGE.sub("", text)
    text = MD_SYM.sub(" ", text)
    text = WS.sub(" ", text)
    return text.strip().lower()


def block_hash(text: str) -> str:
    return hashlib.sha1(normalize(text).encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------- 마크다운 섹션 분해

HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def split_sections(md: str):
    """(level, title, body_lines) 목록. 헤딩 앞 프리앰블은 level 0."""
    sections = []
    cur = [0, "(preamble)", []]
    in_code = False
    for line in md.splitlines():
        if line.lstrip().startswith("```"):
            in_code = not in_code
            cur[2].append(line)
            continue
        m = None if in_code else HEADING.match(line)
        if m:
            sections.append(cur)
            cur = [len(m.group(1)), m.group(2).strip(), []]
        else:
            cur[2].append(line)
    sections.append(cur)
    return [(lv, t, "\n".join(body).strip()) for lv, t, body in sections]


def word_count(text: str) -> int:
    return len(normalize(text).split())


# ---------------------------------------------------------------- 인벤토리

def classify_source(path: Path) -> str:
    p = path.as_posix()
    if "20_Regional_Chapters" in p:
        return "city-guide"
    if "30_Reader_Edition" in p:
        return "reader-edition"
    if "10_Core" in p:
        return "core"
    if "00_Governance" in p:
        return "governance"
    if "OPERATIONS" in p:
        return "operations"
    if "ASSETS" in p:
        return "assets-register"
    return "reference"


def inventory_markdown():
    rows = []
    for path in sorted(SOURCE.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for idx, (lv, title, body) in enumerate(split_sections(text)):
            if not body and lv == 0:
                continue
            rows.append({
                "contentId": f"{path.stem}#{idx:03d}",
                "filePath": rel,
                "headingLevel": lv,
                "sectionTitle": title,
                "contentType": classify_source(path),
                "wordCount": word_count(body),
                "linkCount": len(LINK.findall(body)),
                "imageCount": len(IMG.findall(body)),
                "hash": block_hash(body) if body else "",
                "_body": body,
            })
    return rows


TITLE_RE = re.compile(r"<title>([^<]*)</title>", re.I)
META_REFRESH = re.compile(r'http-equiv=["\']refresh["\']', re.I)
TAG = re.compile(r"<[^>]+>")
SCRIPT_STYLE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.I | re.S)


def inventory_site():
    rows = []
    for path in sorted(SITE.rglob("*.html")):
        rel = path.relative_to(ROOT).as_posix()
        html = path.read_text(encoding="utf-8", errors="replace")
        title = (TITLE_RE.search(html) or [None, ""])[1] if TITLE_RE.search(html) else ""
        is_redirect = bool(META_REFRESH.search(html))
        body = TAG.sub(" ", SCRIPT_STYLE.sub(" ", html))
        rows.append({
            "route": "/" + path.relative_to(SITE).as_posix(),
            "filePath": rel,
            "pageTitle": WS.sub(" ", title).strip(),
            "status": "redirect" if is_redirect else "page",
            "wordCount": len(WS.sub(" ", body).split()),
            "sizeKB": round(path.stat().st_size / 1024, 1),
        })
    return rows


# ---------------------------------------------------------------- 중복 탐지

def detect_duplicates(rows, min_words=25, near_threshold=0.60):
    """섹션 단위 exact(동일 해시) + near(difflib 유사도) 그룹."""
    blocks = [r for r in rows if r["wordCount"] >= min_words]

    groups = []
    by_hash = {}
    for r in blocks:
        by_hash.setdefault(r["hash"], []).append(r)
    exact_done = set()
    for h, members in by_hash.items():
        if len(members) > 1:
            groups.append(("D1-exact", 1.0, members))
            exact_done.update(id(m) for m in members)

    rest = [r for r in blocks if id(r) not in exact_done]
    norm = {id(r): normalize(r["_body"]) for r in rest}
    used = set()
    pairs = []
    for i, a in enumerate(rest):
        na = norm[id(a)]
        for b in rest[i + 1:]:
            # 같은 파일 안 인접 섹션 잡음 방지: 파일이 같고 제목도 같으면만 스킵 안 함
            nb = norm[id(b)]
            if abs(len(na) - len(nb)) / max(len(na), len(nb), 1) > 0.5:
                continue
            sm = difflib.SequenceMatcher(None, na, nb)
            if sm.real_quick_ratio() < near_threshold or sm.quick_ratio() < near_threshold:
                continue
            ratio = sm.ratio()
            if ratio >= near_threshold:
                pairs.append((ratio, a, b))
    # 쌍을 그룹으로 병합 (union-find 간이)
    parent = {}

    def find(x):
        while parent.get(x, x) != x:
            parent[x] = parent.get(parent[x], parent[x])
            x = parent[x]
        return x

    def union(x, y):
        parent.setdefault(x, x)
        parent.setdefault(y, y)
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    score = {}
    for ratio, a, b in pairs:
        union(id(a), id(b))
        score[(id(a), id(b))] = ratio
    clusters = {}
    obj = {id(r): r for r in rest}
    for ratio, a, b in pairs:
        root = find(id(a))
        clusters.setdefault(root, set()).update([id(a), id(b)])
    for root, ids in clusters.items():
        members = [obj[i] for i in ids]
        best = max(s for k, s in score.items() if k[0] in ids or k[1] in ids)
        if best >= 0.95:
            kind = "D2-near-95"
        elif best >= 0.80:
            kind = "D2-near-80"
        else:
            kind = "D3-partial-60"
        groups.append((kind, round(best, 3), members))
    return groups


def detect_boilerplate(min_files=3, min_len=20):
    """여러 파일에서 반복되는 동일 문장(정규화 후)."""
    seen = {}
    for path in sorted(SOURCE.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        for line in {normalize(l) for l in text.splitlines()}:
            if len(line) >= min_len and not line.startswith("|"):
                seen.setdefault(line, set()).add(rel)
    return sorted(
        ((line, files) for line, files in seen.items() if len(files) >= min_files),
        key=lambda x: -len(x[1]),
    )


# ---------------------------------------------------------------- 제목 감사

def audit_headings(rows):
    thin = [r for r in rows if r["headingLevel"] >= 2 and 0 < r["wordCount"] < 15]
    deep = [r for r in rows if r["headingLevel"] >= 4]
    empty = [r for r in rows if r["headingLevel"] >= 2 and r["wordCount"] == 0]
    return thin, deep, empty


# ---------------------------------------------------------------- main

def main():
    DATA.mkdir(exist_ok=True)
    md_rows = inventory_markdown()
    site_rows = inventory_site()

    with (DATA / "content-inventory.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=[
            "contentId", "filePath", "headingLevel", "sectionTitle",
            "contentType", "wordCount", "linkCount", "imageCount", "hash"])
        w.writeheader()
        for r in md_rows:
            w.writerow({k: r[k] for k in w.fieldnames})

    with (DATA / "site-page-inventory.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["route", "filePath", "pageTitle", "status", "wordCount", "sizeKB"])
        w.writeheader()
        w.writerows(site_rows)

    groups = detect_duplicates(md_rows)
    gid = 0
    with (DATA / "content-duplicate-matrix.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["duplicateGroupId", "duplicateType", "similarityScore",
                    "filePath", "sectionTitle", "wordCount", "recommendedAction", "notes"])
        for kind, ratio, members in sorted(groups, key=lambda g: -g[1]):
            gid += 1
            for m in sorted(members, key=lambda r: r["filePath"]):
                w.writerow([f"G{gid:03d}", kind, ratio, m["filePath"],
                            m["sectionTitle"], m["wordCount"], "", ""])

    boiler = detect_boilerplate()
    with (DATA / "content-boilerplate.csv").open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["fileCount", "sentence", "files"])
        for line, files in boiler:
            w.writerow([len(files), line[:200], "; ".join(sorted(files))])

    thin, deep, empty = audit_headings(md_rows)
    stats = {
        "sourceFiles": len({r["filePath"] for r in md_rows}),
        "sourceSections": len(md_rows),
        "sourceWords": sum(r["wordCount"] for r in md_rows),
        "sitePages": sum(1 for r in site_rows if r["status"] == "page"),
        "siteRedirects": sum(1 for r in site_rows if r["status"] == "redirect"),
        "duplicateGroups": gid,
        "exactGroups": sum(1 for k, _, _ in groups if k == "D1-exact"),
        "near95Groups": sum(1 for k, _, _ in groups if k == "D2-near-95"),
        "near80Groups": sum(1 for k, _, _ in groups if k == "D2-near-80"),
        "partialGroups": sum(1 for k, _, _ in groups if k == "D3-partial-60"),
        "boilerplateSentences": len(boiler),
        "thinSections": len(thin),
        "deepHeadings": len(deep),
        "emptySections": len(empty),
    }
    (DATA / "audit-stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    print("\nwrote:", ", ".join(p.name for p in sorted(DATA.glob('*.csv'))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
