#!/usr/bin/env python3
"""장소 장문을 챕터 원고에서 정식 데이터로 승격시킨다.

    source/CURRENT/20_Regional_Chapters/*.md   (장소 서술이 갇혀 있던 곳)
        ↓  한 번 옮긴다
    source/CURRENT/30_Places/<slug>.md         (정본)

왜. 예전 빌드는 챕터 마크다운에서 장소 절을 정규식으로 잘라내고, 실패하면
**이미 빌드된 HTML 을 다시 파싱해** 220자 발췌를 만들었다. 세 가지 휴리스틱
가드가 조용히 실패했고 (3줄 미만·2500자 초과·하위 절 포함), 그때마다 장소
페이지의 내용이 달라졌다. 원고 제목을 한 글자 고치면 결과가 바뀌었다.

한 장소 = 한 파일로 만들면 그 불확실성이 사라진다.

    1 Place = 1 canonical long-form guide

이 스크립트는 **한 번만** 돌린다. 그 뒤로는 30_Places/ 가 정본이고, 챕터
원고의 해당 절은 지운다. 두 곳에 같은 글이 남으면 사본이 되살아난다.

    python3 build/promote_places.py --dry-run   # 무엇이 옮겨질지만 본다
    python3 build/promote_places.py             # 실제로 쓴다
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "source" / "CURRENT" / "20_Regional_Chapters"
OUT_DIR = ROOT / "source" / "CURRENT" / "30_Places"
REGISTRY_MD = ROOT / "source" / "ASSETS" / "91_Place_Registry_v1.0.md"

CHAPTER_REGION = {
    "04": "barcelona", "05": "girona", "06": "nice", "07": "aix",
    "08": "luberon", "09": "avignon", "10": "lyon", "11": "paris",
}

HEADING = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
# 제목에 붙는 토큰·번호를 떼어낸다. {{grade:essential|필수}} · "8.6 " 같은 것.
TOKEN = re.compile(r"\{\{[^}]*\}\}")
NUMPREFIX = re.compile(r"^\d+(\.\d+)*\.?\s+")

# 하위 절 이름 → 목표 층. 원고가 이미 이 세 갈래로 쓰여 있다.
WHY_GO = re.compile(r"^(무엇인가|왜 |왜$|어떤 곳)")
DEEP = re.compile(r"^(핵심|소장품|배경|역사|건축|더 보기)")
PRACTICAL = re.compile(r"^(실용|실무|현장|접근|가는 법)")


def norm(s: str) -> str:
    """제목 대조용 키. 발음기호·괄호·번호·토큰·공백을 지운 소문자 영숫자."""
    s = TOKEN.sub("", s)
    s = NUMPREFIX.sub("", s)
    s = re.sub(r"\([^)]*\)", "", s)
    s = s.split("—")[0].split("–")[0].split(" - ")[0]
    # NFD 로 풀어 발음기호만 떼고 NFC 로 되붙인다. NFKD 를 쓰면 한글이
    # 자모로 분해되고, 자모는 [가-힣] 범위 밖이라 통째로 사라진다.
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"[^a-z0-9가-힣]", "", s.lower())


def load_registry() -> list[dict]:
    rows, region = [], None
    for line in REGISTRY_MD.read_text(encoding="utf-8").splitlines():
        h = re.match(r"^##\s+([a-z]+)\s*\((\d+)\)", line)
        if h:
            region = CHAPTER_REGION.get(h.group(2))
            continue
        m = re.match(r"^\|\s*`([a-z0-9-]+)`\s*\|(.*)$", line)
        if not m or region is None:
            continue
        c = [x.strip() for x in m.group(2).split("|")]
        def cell(i):
            v = c[i] if i < len(c) else ""
            return None if v in ("", "—", "-") else v
        rows.append({
            "slug": m.group(1), "name": cell(0) or m.group(1),
            "kind": cell(1) or "spot", "grade": cell(2),
            "head": cell(5), "region": region,
        })
    return rows


def split_sections(text: str) -> list[dict]:
    """마크다운을 (레벨, 제목, 본문줄) 목록으로. 표·인용 안의 # 는 건드리지 않는다."""
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


def extract(region: str, path: Path, by_key: dict) -> tuple[list[dict], list[str]]:
    """장소 절을 뽑는다. 매칭 안 된 제목은 전부 돌려준다 — 조용히 버리지 않는다."""
    secs = split_sections(path.read_text(encoding="utf-8"))
    found, unmatched = [], []

    for i, sec in enumerate(secs):
        key = norm(sec["title"])
        row = by_key.get((region, key))
        if row is None:
            continue

        # 이 절의 끝 = 같거나 더 높은 레벨의 다음 제목
        sub = []
        for nxt in secs[i + 1:]:
            if nxt["level"] <= sec["level"]:
                break
            sub.append(nxt)

        lead = "\n".join(sec["lines"]).strip()
        why, deep, practical = [], [], []
        for s in sub:
            block = f"{'#' * s['level']} {s['title']}\n" + "\n".join(s["lines"])
            t = TOKEN.sub("", s["title"]).strip()
            if WHY_GO.match(t):
                why.append("\n".join(s["lines"]).strip())
            elif PRACTICAL.match(t):
                practical.append(block.strip())
            elif DEEP.match(t):
                deep.append(block.strip())
            else:
                deep.append(block.strip())

        found.append({
            "chars": len(lead) + sum(len(x) for x in why + deep + practical),
            "row": row,
            "lead": lead,
            "why_go": "\n\n".join(x for x in why if x).strip(),
            "deep": "\n\n".join(x for x in deep if x).strip(),
            "practical": "\n\n".join(x for x in practical if x).strip(),
            "heading": sec["title"],
            "source": f"{path.relative_to(ROOT)}",
        })

    return found, unmatched


def summarize(text: str, limit: int = 110) -> str:
    """카드에 쓸 한 줄. 원문 첫 문장을 그대로 쓴다 — 새로 쓰지 않는다."""
    plain = re.sub(r"\{\{[^}]*\}\}", "", text)
    plain = re.sub(r"[*_`>#|]", "", plain)
    plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", plain)
    for line in plain.splitlines():
        line = line.strip()
        if len(line) < 20 or line.startswith("-") or set(line) <= set("- "):
            continue
        sentence = re.split(r"(?<=[.다])\s", line)[0].strip()
        return sentence if len(sentence) <= limit else sentence[:limit].rstrip() + "…"
    return ""


def write_place(item: dict, dry: bool) -> Path:
    row = item["row"]
    summary = summarize(item["why_go"] or item["lead"])
    fm = [
        "---",
        f'slug: {row["slug"]}',
        f'name: "{row["name"]}"',
        f'region: {row["region"]}',
        f'kind: {row["kind"]}',
    ]
    if row["grade"]:
        fm.append(f'grade: "{row["grade"]}"')
    if summary:
        fm.append(f'summary: "{summary}"')
    fm += [f'source: {item["source"]}', "---", ""]

    parts = list(fm)
    if item["why_go"]:
        parts += ["## 왜 가는가", "", item["why_go"], ""]
    if item["deep"]:
        parts += ["## 더 깊이", "", item["deep"], ""]
    if item["practical"]:
        parts += ["## 실용", "", item["practical"], ""]
    if not (item["why_go"] or item["deep"]) and item["lead"]:
        parts += [item["lead"], ""]

    out = OUT_DIR / f"{row['slug']}.md"
    if not dry:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    registry = load_registry()
    by_key: dict[tuple[str, str], dict] = {}
    for row in registry:
        for candidate in filter(None, (row["head"], row["name"], row["slug"])):
            key = norm(candidate)
            if not key:
                continue   # 빈 키 하나가 그 지역의 모든 제목을 삼킨다
            by_key.setdefault((row["region"], key), row)

    # 슬러그마다 절을 모은다. 한 장소가 원고 여러 곳에 흩어져 있으면
    # 버리지 않고 합친다 — 콘텐츠 손실 0 이 조건이다.
    collected: dict[str, list[dict]] = {}
    unmatched: list[str] = []
    for path in sorted(CHAPTERS.glob("*.md")):
        num = path.name.split("_")[0]
        region = CHAPTER_REGION.get(num)
        if region is None:
            continue
        found, misses = extract(region, path, by_key)
        unmatched += misses
        for item in found:
            collected.setdefault(item["row"]["slug"], []).append(item)

    promoted, merged = [], 0
    for slug, items in collected.items():
        # 긴 절이 앞에 오게 둔다 — 가장 충실한 서술이 본문의 머리가 된다
        items.sort(key=lambda x: -x["chars"])
        total = sum(i["chars"] for i in items)
        if total < 120:
            unmatched.append(f"{slug}: 전체 본문 {total}자 — 장문으로 보기 어려워 건너뜀")
            continue
        if len(items) > 1:
            merged += 1
        item = {
            "row": items[0]["row"],
            "lead": items[0]["lead"],
            "why_go": "\n\n".join(i["why_go"] for i in items if i["why_go"]).strip(),
            "deep": "\n\n".join(i["deep"] for i in items if i["deep"]).strip(),
            "practical": "\n\n".join(i["practical"] for i in items if i["practical"]).strip(),
            "source": " · ".join(sorted({i["source"] for i in items})),
        }
        if not item["why_go"] and not item["deep"]:
            item["deep"] = "\n\n".join(i["lead"] for i in items if i["lead"]).strip()
        write_place(item, args.dry_run)
        promoted.append(item)

    by_region: dict[str, int] = {}
    for item in promoted:
        by_region[item["row"]["region"]] = by_region.get(item["row"]["region"], 0) + 1

    print(f"승격 {len(promoted)} / 명부 {len(registry)}  (여러 절을 병합한 장소 {merged}개)")
    for region in CHAPTER_REGION.values():
        total = sum(1 for r in registry if r["region"] == region)
        print(f"  {region:10s} {by_region.get(region, 0):3d} / {total}")

    covered = {i["row"]["slug"] for i in promoted}
    absent = [r for r in registry if r["slug"] not in covered]
    print(f"\n장문 없는 장소 {len(absent)}건 — 원고에 해당 절이 없다:")
    for r in absent[:40]:
        print(f"  {r['region']:10s} {r['slug']:38s} {r['name']}")
    if len(absent) > 40:
        print(f"  … 외 {len(absent) - 40}건")

    if unmatched:
        print(f"\n건너뛴 절 {len(unmatched)}건:")
        for u in unmatched[:20]:
            print("  " + u)

    if args.dry_run:
        print("\n(--dry-run — 파일을 쓰지 않았다)")
    else:
        print(f"\n{OUT_DIR.relative_to(ROOT)} 에 {len(promoted)}개 파일을 썼다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
