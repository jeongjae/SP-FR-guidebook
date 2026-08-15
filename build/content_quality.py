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
# `영업소`(렌터카 지점)는 운영정보가 아니라 장소다 — 영업시간·영업일만 잡는다.
OPERATION_RE = re.compile(r"(개관|운영시간|휴관|휴무|입장료|요금|€\s?\d|무료입장|영업(?!소))")
NUMBER_RE = re.compile(r"(€\s?\d|\d{1,2}:\d{2}|\d+\s?분|\d+시|\d+\s?유로)")
# 근거로 인정하는 표기. `계획가`·`확정` 은 **날짜를 요구한다** — 상속을 허용하는
# 대신 통과 문턱을 좁혔다. 맨 '확인' 두 글자로는 통과하지 않는다.
EVIDENCE_RE = re.compile(
    r"(공식\s*(사이트|페이지|안내|정보|출처)|출처\s*[:：]|https?://|badge:pending"
    r"|20\d\d-\d\d(-\d\d)?\s*확인|20\d\d년?\s*\d{1,2}월\s*확인|계획가\(20\d\d-\d\d"
    r"|확정\(20\d\d-\d\d|출발 전 재확인|\[재확인\]|기록\(20\d\d-\d\d"
    r"|복수 출처 확인|\|\s*확인\s*\|)")

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
    """운영 블록(목록·표)을 뺀 서술 자수.

    인용 블록(>)은 이 원고에서 팁·해설 카드로 쓰인다 — 독자에게는 서술이다.
    다만 출처 쪽지·배지 줄은 서술이 아니라 근거 표기이므로 뺀다.
    """
    keep = []
    for line in body.splitlines():
        s = line.strip()
        # `- ` `* ` 만 목록이다 — `**볼드` 로 시작하는 문단을 목록으로 오인하지 않는다.
        if not s or s.startswith(("| ", "|-", "- ", "* ")) or s.startswith("#") or s == "|":
            continue
        if s.startswith(">"):
            inner = s.lstrip("> ").strip()
            if (not inner or inner.startswith(("출처", "{{badge", "가격은 **계획가"))
                    or "계획가(20" in inner[:30]):
                continue
            keep.append(inner)
            continue
        keep.append(s)
    return len("".join(keep))


def walk_with_context(text: str):
    """(줄번호, 줄, 근거유무) — 근거는 그 줄이 속한 **블록**에서 상속된다.

    사람이 읽는 단위를 따른다.
    - 문단은 한 덩어리다. 문단 어느 줄에 출처가 있으면 그 문단 전체가 근거를 갖는다.
    - 표·목록은 바로 앞 문단(또는 인용 쪽지)과 표 머리글에서 상속한다.
    - 하위 헤딩은 상위 헤딩의 근거를 물려받는다 — `## 13. 레스토랑` 아래
      `계획가(2026-08 조사)` 쪽지가 있으면 `### 13.2` 도 그 안이다.

    상속을 허용하는 대신 **근거로 인정하는 표기는 좁다** (EVIDENCE_RE) —
    `계획가`·`확정` 은 날짜를 요구하고, 맨 '확인' 두 글자로는 통과하지 않는다.
    """
    lines = text.splitlines()
    n_lines = len(lines)
    result = [False] * (n_lines + 1)

    stack = []          # [(heading_level, evidence)]
    prelude_ev = False
    table_ev = False
    in_table = False
    para: list[int] = []
    para_ev = False

    def flush_para():
        nonlocal para, para_ev, prelude_ev
        if para:
            for idx in para:
                result[idx] = result[idx] or para_ev or prelude_ev or _ancestor()
            # 근거 쪽지는 다음 헤딩까지 산다. 중간의 라벨 문단('**주문 예시 A**')이
            # 쪽지를 지워버리면 바로 아래 목록이 근거를 잃는다.
            prelude_ev = prelude_ev or para_ev
        para, para_ev = [], False

    def _ancestor():
        return any(ev for _, ev in stack)

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        own = bool(EVIDENCE_RE.search(line))

        if stripped.startswith("#"):
            flush_para()
            level = len(stripped) - len(stripped.lstrip("#"))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, own))
            prelude_ev = table_ev = in_table = False
            result[i] = own or _ancestor()
            continue

        if not stripped:
            flush_para()
            in_table = False
            continue

        if stripped.startswith("|"):
            flush_para()
            if not in_table:                       # 표의 첫 줄 = 머리글
                in_table, table_ev = True, own or prelude_ev
            result[i] = own or table_ev or _ancestor()
            continue

        in_table = False
        if stripped.startswith(">"):
            # 인용 쪽지는 뒤따르는 표·목록의 근거가 된다
            prelude_ev = own or prelude_ev
            result[i] = own or prelude_ev or _ancestor()
            continue

        if stripped.startswith(("- ", "* ", "1.")):
            result[i] = own or prelude_ev or _ancestor()
            continue

        para.append(i)
        para_ev = para_ev or own

    flush_para()
    for i, line in enumerate(lines, 1):
        yield i, line, result[i]


def has_element(body: str, aliases) -> bool:
    return any(re.search(rf"(^|\n)\s*[-*]?\s*\*{{0,2}}{a}", body) for a in aliases)


def collect():
    rows = registry_rows()
    spots = [r for r in rows if r["type"] == "spot"]
    grades = Counter(r["grade"] for r in rows)

    # ---- C1 커버리지
    no_body = [r["name"] for r in spots if r["body"] in EMPTY]
    no_wiki = [r["name"] for r in rows if r["wiki"] in EMPTY]

    # ---- C2 밀도 · C4 구조 — **독자가 읽는 챕터 등급 절**을 잰다.
    # dossier(90) 는 사이트에 렌더되지 않는 빌드 보조 문서다 (공식 URL 의 소스).
    # 안 보이는 문서의 밀도는 품질이 아니다 — R3 에서 측정 대상을 교정했다 (2026-08-14).
    grade_head = re.compile(r"^(#{2,5}) (.+?) \{\{grade:(\w+)\|", re.M)

    def graded_section(text, m):
        """등급 헤딩부터 다음 실질 헤딩까지. 사진·VISUAL 헤딩은 절을 끊지 않는다."""
        level = len(m.group(1))
        rest = text[m.end():]
        for h in re.finditer(rf"^(#{{2,{level}}}) (.+)$", rest, re.M):
            if h.group(2).startswith(("{{VISUAL", "사진 에셋")):
                continue
            return rest[:h.start()]
        return rest

    sections = {}          # 헤딩 → 가장 긴 절 (실행표 헤딩과 상세 절이 같은 이름일 때)
    for path in sorted(CHAPTER_DIR.glob("*.md")):
        text = read(path)
        for m in grade_head.finditer(text):
            name = m.group(2).strip()
            body = graded_section(text, m)
            if name not in sections or prose_length(body) > prose_length(sections[name][1]):
                sections[name] = (path.name, body)

    heading_grade = {r["heading"]: r["grade"] for r in rows if r["heading"] not in EMPTY}
    lengths = [prose_length(b) for _, b in sections.values()]
    total_lengths = [len(b) for _, b in sections.values()]
    below, element_gaps = [], Counter()
    for name, (fname, body) in sections.items():
        grade = heading_grade.get(name, "선택")
        floor = max(GRADE_MIN_CHARS.get(grade, 350), 350)
        pl = prose_length(body)
        if pl < floor:
            below.append({"place": name, "grade": grade, "chars": pl,
                          "floor": floor, "file": fname})
        # C4 — why-go(왜 이 여행인가) 와 정체성 서술을 절 안에서 본다.
        if pl < 200:
            element_gaps["why_go"] += 1
        first = body.strip().split("\n", 1)[0].strip()
        if len(first) < 30 and pl < 350:
            element_gaps["정체성"] += 1

    # dossier ↔ 레지스트리 이름 대조는 유지한다 (공식 URL 연결이 여기 걸린다).
    dossiers = dossier_sections()
    name_set = {r["name"] for r in rows}
    unmatched = [t for t, _ in dossiers if t not in name_set]

    # ---- C3 근거
    op_total = op_evidenced = 0
    unsourced = []
    for path in sorted(CHAPTER_DIR.glob("*.md")):
        for n, line, evidence in walk_with_context(read(path)):
            if OPERATION_RE.search(line) and NUMBER_RE.search(line):
                op_total += 1
                if evidence:
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
        "C2": {"dossiers": len(sections),
               "median": int(statistics.median(lengths)) if lengths else 0,
               "min": min(lengths) if lengths else 0,
               "max": max(lengths) if lengths else 0,
               "total_median": result_c2_total,  # 표·목록 포함 전체 자수
               "below_floor": len(below), "below": below[:90],
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
# R1 (2026-08-14): 근거 없는 운영정보를 0 으로 잠근다. 앞으로 출처·확인일·pending
# 없이 개관시간이나 요금을 새로 쓰면 이 게이트에서 멈춘다.
GATES: dict[str, tuple[str, int]] = {
    "무근거 운영정보": ("C3.unsourced", 0),
    # R2 (2026-08-14): 모든 spot 이 본문을 갖고, dossier 는 전부 레지스트리와 이어진다.
    "본문 없는 spot": ("C1.no_body", 0),
    "dossier 이름 불일치": ("C2.unmatched", 0),
    # R3 (2026-08-14): 등급별 서술 하한. 새 장소를 스텁으로 추가하면 여기서 멈춘다.
    "등급별 분량 하한 미달": ("C2.below_floor", 0),
}


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
        f"| C2 | 등급 절(독자 화면) 서술 중앙값 | **{c2['median']}자** (표·목록 포함 {c2['total_median']}자) |",
        f"| C2 | 등급별 분량 하한 미달 절 | **{c2['below_floor']}** / {c2['dossiers']} |",
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
    print(f"C2 밀도    : 등급 절 {c2['dossiers']} · 서술 중앙값 {c2['median']}자 "
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
