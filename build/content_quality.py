#!/usr/bin/env python3
"""콘텐츠 품질 스코어카드 — 상용 가이드북 기준 C1~C6 을 measurement 한다.

`docs/CONTENT_QUALITY_PLAN_v1.0.md` 의 6축을 그대로 계산한다. 계획서에 적힌
baseline 은 이 스크립트가 재현할 수 있어야 한다 — 재현되지 않는 수치는
목표로 쓸 수 없다.

    python3 build/content_quality.py            # 스코어카드 출력
    python3 build/content_quality.py --json     # 기계 판독용
    python3 build/content_quality.py --write    # docs/CONTENT_SCORECARD.md 갱신
    python3 build/content_quality.py --gate     # 하한 위반 시 exit 1 (라운드마다 조인다)

⚠ 이 스크립트는 **셀 수 있는 것만** 판정한다. 문장의 읽는 맛, 편집 판단의
설득력, 사진의 적절성은 여기서 통과해도 확인된 것이 아니다.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "source"
REGISTRY = SOURCE / "ASSETS" / "91_Place_Registry_v1.0.md"
DOSSIERS = SOURCE / "ASSETS" / "90_Regional_Context_and_Place_Dossier_Compendium_v1.0.md"
CHAPTER_DIR = SOURCE / "CURRENT" / "20_Regional_Chapters"
PHOTO_CANDIDATES = ROOT / "data" / "images" / "photo-candidates.json"
SCORECARD = ROOT / "docs" / "CONTENT_SCORECARD.md"

EMPTY = {"—", "-", ""}

# 등급별 서술 분량 하한 (계획서 §2). 운영 블록을 뺀 순수 서술 기준이다.
GRADE_MIN_CHARS = {"필수": 700, "우선 추천": 500, "선택": 350, "대체": 350, "비추천": 0, "미정": 0}

# dossier 7요소 — 라벨 표기가 원고마다 달라 별칭을 함께 본다.
DOSSIER_ELEMENTS = {
    "정체성": None,                       # 헤딩 다음 서술 문장
    "why_go": None,                       # 왜 우리에게 의미가 있는가 (서술 문단)
    "방문": ("방문", "가는 법", "접근"),
    "관람": ("관람", "볼 것", "포인트"),
    "체류": ("체류", "소요"),
    "요금·예약": ("요금", "예약", "티켓"),
    "주의": ("주의", "혼잡", "복장"),
    "출처": ("공식", "출처"),
}

# C3 — 운영정보를 말하는 줄인가. 우리 일정 시각(계획값)은 대상이 아니다.
OPERATION_RE = re.compile(r"(개관|운영시간|휴관|휴무|입장료|요금|€\s?\d|무료입장|영업)")
NUMBER_RE = re.compile(r"(€\s?\d|\d{1,2}:\d{2}|\d+\s?분|\d+시|\d+\s?유로)")
EVIDENCE_RE = re.compile(r"(공식|출처|badge:pending|https?://|재확인|확인)")

# C6 — 본문에 남으면 안 되는 잔재
CANCELLED_TERMS = ("Hamlet", "Il Barbiere", "Este Mundo")
CANDIDATE_RE = re.compile(r"후보")

PENDING_RE = re.compile(r"\{\{badge:pending\|([^}]*)\}\}")
# pending 은 종류가 섞이면 현장에서 무엇을 해야 할지 알 수 없다 (계획서 M10).
PENDING_KINDS = {
    "재확인": ("재확인", "확인"),
    "결정": ("결정", "선정", "변경"),
    "조사": ("조사", "미정", "검토"),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def registry_rows():
    """장소 레지스트리 표 → dict 목록. 정본은 이 MD 다."""
    rows = []
    for line in read(REGISTRY).splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 7:
            continue
        rows.append({
            "slug": cells[0].strip("`"), "name": cells[1], "type": cells[2],
            "grade": cells[3].rstrip("*"), "pin": cells[4], "body": cells[5],
            "heading": cells[6], "wiki": cells[7] if len(cells) > 7 else "—",
        })
    return rows


def dossier_sections():
    """장소 dossier → (제목, 본문) 목록."""
    parts = re.split(r"^## ", read(DOSSIERS), flags=re.M)[1:]
    out = []
    for part in parts:
        head, _, body = part.partition("\n")
        out.append((head.strip(), body))
    return out


def prose_length(body: str) -> int:
    """운영 블록(`- 방문:` 류 목록)과 표를 뺀 순수 서술 자수."""
    keep = []
    for line in body.splitlines():
        s = line.strip()
        if not s or s.startswith(("|", "-", "*", ">")) or s.startswith("#"):
            continue
        keep.append(s)
    return len("".join(keep))


def has_element(body: str, aliases) -> bool:
    return any(re.search(rf"(^|\n)\s*[-*]?\s*\*{{0,2}}{a}", body) for a in aliases)


def collect():
    rows = registry_rows()
    spots = [r for r in rows if r["type"] == "spot"]
    grades = Counter(r["grade"] for r in rows)

    # ---- C1 커버리지
    no_body = [r["name"] for r in spots if r["body"] in EMPTY]
    no_wiki = [r["name"] for r in rows if r["wiki"] in EMPTY]

    # ---- C2 밀도 · C4 구조
    dossiers = dossier_sections()
    lengths = [prose_length(b) for _, b in dossiers]
    total_lengths = [len(b) for _, b in dossiers]
    grade_by_name = {r["name"]: r["grade"] for r in rows}
    below, element_gaps, unmatched = [], Counter(), []
    for title, body in dossiers:
        # 레지스트리에 없는 제목을 '미정'으로 흘려보내면 하한 검사를 통째로 빠져나간다.
        if title not in grade_by_name:
            unmatched.append(title)
        grade = grade_by_name.get(title, "우선 추천")
        floor = max(GRADE_MIN_CHARS.get(grade, 350), 350)
        if prose_length(body) < floor:
            below.append({"place": title, "grade": grade,
                          "chars": prose_length(body), "floor": floor})
        for key, aliases in DOSSIER_ELEMENTS.items():
            if aliases is None:
                continue
            if not has_element(body, aliases):
                element_gaps[key] += 1
        # 정체성·why-go 는 라벨이 아니라 서술로 판정한다.
        first = body.strip().split("\n", 1)[0].strip()
        if len(first) < 40:
            element_gaps["정체성"] += 1
        if prose_length(body) < 200:
            element_gaps["why_go"] += 1

    # ---- C3 근거
    op_total = op_evidenced = 0
    unsourced = []
    for path in sorted(CHAPTER_DIR.glob("*.md")):
        for n, line in enumerate(read(path).splitlines(), 1):
            if OPERATION_RE.search(line) and NUMBER_RE.search(line):
                op_total += 1
                if EVIDENCE_RE.search(line):
                    op_evidenced += 1
                else:
                    unsourced.append({"file": path.name, "line": n,
                                      "text": line.strip()[:100]})

    # ---- C6 잔재 · pending 분류
    cancelled = candidate = 0
    pending_kinds = Counter()
    for path in sorted(CHAPTER_DIR.glob("*.md")):
        text = read(path)
        cancelled += sum(text.count(t) for t in CANCELLED_TERMS)
        candidate += len(CANDIDATE_RE.findall(text))
        for label in PENDING_RE.findall(text):
            kind = next((k for k, words in PENDING_KINDS.items()
                         if any(w in label for w in words)), "미분류")
            pending_kinds[kind] += 1

    # ---- 사진 커버리지
    photo_ids = set()
    if PHOTO_CANDIDATES.exists():
        payload = json.loads(read(PHOTO_CANDIDATES))
        photo_ids = {c["placeId"] for c in payload.get("candidates", [])
                     if c.get("selected")}
    essential = [r for r in spots if r["grade"] == "필수"]
    photo_missing_essential = [r["name"] for r in essential
                               if r["slug"] not in photo_ids]
    photo_missing_all = [r["name"] for r in spots if r["slug"] not in photo_ids]

    # ---- 챕터 분량
    chapters = {p.name: len(read(p)) for p in sorted(CHAPTER_DIR.glob("*.md"))}

    result_c2_total = int(statistics.median(total_lengths)) if total_lengths else 0
    return {
        "C1": {"spots": len(spots), "no_body": len(no_body), "no_body_names": no_body,
               "no_wiki": len(no_wiki), "grades": dict(grades)},
        "C2": {"dossiers": len(dossiers),
               "median": int(statistics.median(lengths)) if lengths else 0,
               "min": min(lengths) if lengths else 0,
               "max": max(lengths) if lengths else 0,
               "total_median": result_c2_total,  # 표·목록 포함 전체 자수
               "below_floor": len(below), "below": below[:20],
               "unmatched": len(unmatched), "unmatched_names": unmatched},
        "C3": {"operational_lines": op_total, "evidenced": op_evidenced,
               "unsourced": op_total - op_evidenced,
               "rate": round(op_evidenced / op_total, 4) if op_total else 1.0,
               "samples": unsourced[:15]},
        "C4": {"element_gaps": dict(element_gaps)},
        "C6": {"cancelled_mentions": cancelled, "candidate_mentions": candidate,
               "pending_by_kind": dict(pending_kinds),
               "pending_total": sum(pending_kinds.values())},
        "photos": {"spots": len(spots), "with_photo": len(spots) - len(photo_missing_all),
                   "missing": len(photo_missing_all),
                   "essential": len(essential),
                   "essential_missing": len(photo_missing_essential),
                   "essential_missing_names": photo_missing_essential},
        "chapters": chapters,
    }


# 라운드가 끝날 때마다 그 라운드의 지표를 여기서 조인다 (계획서 §4 회귀 방지).
# R0 은 측정만 한다 — 지금 잠그면 baseline 자체가 실패한다.
GATES: dict[str, tuple[str, int]] = {}


def gate(data) -> int:
    problems = []
    for key, (path, limit) in GATES.items():
        cursor = data
        for part in path.split("."):
            cursor = cursor[part]
        if cursor > limit:
            problems.append(f"{key}: {cursor} (하한 {limit})")
    if problems:
        print("콘텐츠 품질 게이트 실패:")
        for p in problems:
            print("  " + p)
        return 1
    print(f"콘텐츠 품질 게이트: {len(GATES)}개 지표 이상 없음"
          if GATES else "콘텐츠 품질 게이트: 잠근 지표 없음 (R0 측정 단계)")
    return 0


def render(data) -> str:
    c1, c2, c3, c6, ph = data["C1"], data["C2"], data["C3"], data["C6"], data["photos"]
    lines = [
        "# 콘텐츠 품질 스코어카드",
        "",
        "`python3 build/content_quality.py --write` 가 생성한다. 손으로 고치지 않는다.",
        "기준과 목표치는 `CONTENT_QUALITY_PLAN_v1.0.md` 에 있다.",
        "",
        "## 지표",
        "",
        "| 축 | 지표 | 현재 |",
        "|---|---|---:|",
        f"| C1 | 본문 없는 spot | **{c1['no_body']}** / {c1['spots']} |",
        f"| C1 | 위키 참고 없는 항목 | {c1['no_wiki']} |",
        f"| C1 | dossier ↔ 레지스트리 이름 불일치 | **{c2['unmatched']}** / {c2['dossiers']} |",
        f"| C2 | dossier 서술 중앙값 | **{c2['median']}자** (표·목록 포함 전체 {c2['total_median']}자) |",
        f"| C2 | 등급별 분량 하한 미달 | **{c2['below_floor']}** / {c2['dossiers']} |",
        f"| C3 | 운영정보 줄 | {c3['operational_lines']} |",
        f"| C3 | 근거 표기 | {c3['evidenced']} ({c3['rate']:.0%}) |",
        f"| C3 | **무근거** | **{c3['unsourced']}** |",
        f"| C6 | 취소 공연 잔재 | {c6['cancelled_mentions']} |",
        f"| C6 | `후보` 표기 | {c6['candidate_mentions']} |",
        f"| C6 | pending 미분류 | {c6['pending_by_kind'].get('미분류', 0)} / {c6['pending_total']} |",
        f"| 사진 | 필수 등급 커버리지 | {ph['essential'] - ph['essential_missing']} / {ph['essential']} |",
        f"| 사진 | 전체 spot 커버리지 | {ph['with_photo']} / {ph['spots']} |",
        "",
        "## C4 — dossier 요소 결측",
        "",
        "| 요소 | 결측 |",
        "|---|---:|",
    ]
    for key, count in sorted(data["C4"]["element_gaps"].items(), key=lambda x: -x[1]):
        lines.append(f"| {key} | {count} |")
    lines += [
        "",
        "## dossier ↔ 레지스트리 이름 불일치",
        "",
        "이 제목들은 dossier 로는 존재하지만 레지스트리의 장소와 이어지지 않는다 —",
        "**글은 있는데 그 장소 페이지에서는 보이지 않는다.**",
        "",
        ", ".join(c2["unmatched_names"]) if c2["unmatched_names"] else "없다.",
        "",
        "## 본문 없는 spot",
        "",
        ", ".join(c1["no_body_names"]) if c1["no_body_names"] else "없다.",
        "",
        "## 필수 등급 사진 없음",
        "",
        ", ".join(ph["essential_missing_names"]) if ph["essential_missing_names"] else "없다.",
        "",
        "---",
        "",
        "**이 표가 판정하지 못하는 것**: 문장의 읽는 맛, 편집 판단의 설득력, 사진의 적절성.",
        "전부 통과해도 품질이 확인된 것이 아니다 — 라운드마다 표본을 읽어서 본다.",
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--gate", action="store_true")
    args = ap.parse_args()

    data = collect()
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    if args.write:
        SCORECARD.write_text(render(data), encoding="utf-8")
        print(f"스코어카드 갱신: {SCORECARD.relative_to(ROOT)}")

    c1, c2, c3, c6, ph = data["C1"], data["C2"], data["C3"], data["C6"], data["photos"]
    print(f"C1 커버리지: spot {c1['spots']} · 본문 없음 {c1['no_body']} · 위키 없음 {c1['no_wiki']}")
    print(f"C2 밀도    : dossier {c2['dossiers']} · 서술 중앙값 {c2['median']}자 "
          f"(전체 {c2['total_median']}자) · 하한 미달 {c2['below_floor']} "
          f"· 레지스트리 미매칭 {c2['unmatched']}")
    print(f"C3 근거    : 운영정보 {c3['operational_lines']}줄 · 근거 {c3['evidenced']} "
          f"({c3['rate']:.0%}) · 무근거 {c3['unsourced']}")
    print(f"C4 구조    : 결측 {data['C4']['element_gaps']}")
    print(f"C6 무모순  : 취소 잔재 {c6['cancelled_mentions']} · 후보 {c6['candidate_mentions']} "
          f"· pending {c6['pending_total']} (미분류 {c6['pending_by_kind'].get('미분류', 0)})")
    print(f"사진       : 필수 {ph['essential'] - ph['essential_missing']}/{ph['essential']} "
          f"· 전체 {ph['with_photo']}/{ph['spots']}")
    return gate(data) if args.gate else 0


if __name__ == "__main__":
    sys.exit(main())
