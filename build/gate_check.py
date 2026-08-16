#!/usr/bin/env python3
"""RS Restructure 재작업 게이트 — 기계검사 6종.

사용법:
    python3 build/gate_check.py 10_Lyon_v2.0.md [...]
    python3 build/gate_check.py --all          # 재작업 완료 챕터 전부
    python3 build/gate_check.py --build-only   # 1번만

검사 (RS_RESTRUCTURE_FINAL_RUN_INSTRUCTION_v1.0 §2):
  1 build.py + test_validation.py + hig_check.py, 페이지 수
  2 확정 토큰 생존 가드 (build 로그에서 확인)
  3 이동-전용 자구 대조: 비헤딩 본문 행 중 main 행집합과 일치 ≥95%
  4 창작 스캔: 미소급 행의 사실값이 main 전체 텍스트에 없으면 신규 창작
  5 중복 소진 스캔: 40자 이상 행이 90 컴펜디움에 그대로 있으면 중복
  6 경어체 0건
"""
import argparse
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "source/CURRENT/20_Regional_Chapters"
COMPENDIUM = ROOT / "source/ASSETS/90_Regional_Context_and_Place_Dossier_Compendium_v1.0.md"

VERBATIM_FLOOR = 95.0
DUP_MIN_LEN = 40

# 사실값: 통화 · 시각 · 전화 · 예약코드 · 거리/시간/면적 · 연도 · 날짜
FACT_RE = re.compile(
    r"€\s?\d|\d{1,2}:\d{2}|\+\d{2}\s?\d|\b0[1-9](?:[\s.]?\d{2}){4}\b"
    r"|\b[A-Z0-9]{6,}\b|\d+\s?(?:km|㎡|ha|면|분|시간)\b|\d{4}년|\d{1,2}/\d{1,2}")

def polite_hits(line):
    """경어체 종결어미(-습니다/-ㅂ니다/-습니까)만 잡는다.

    '아이러니다' 처럼 명사 + '다' 인 경우를 오탐하지 않도록,
    '니다/니까' 앞 글자의 종성이 ㅂ(받침 인덱스 17)인지 직접 본다.
    """
    hits = []
    for m in re.finditer(r"([가-힣])(니다|니까)", line):
        ch = m.group(1)
        code = ord(ch) - 0xAC00
        if 0 <= code <= 11171 and code % 28 == 17:   # 종성 ㅂ → 습니다·합니다·입니다…
            hits.append(m.group(0))
    return hits


def sh(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, **kw)


def main_text(name):
    r = sh(["git", "show", f"main:source/CURRENT/20_Regional_Chapters/{name}"])
    if r.returncode != 0:
        return None
    return r.stdout


def norm(s):
    return re.sub(r"\s+", "", s)


def reader_body(text):
    """front matter·코드블록·링크줄·이미지·VISUAL 토큰을 뺀 독자용 본문."""
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"^\s*[-*]?\s*\[?[^\n]*?https?://\S+[^\n]*$", "", text, flags=re.M)
    text = re.sub(r"\{\{VISUAL:[^}]*\}\}", "", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    return norm(text)


def gate1_build():
    out = {}
    r = sh([sys.executable, "build/build.py"])
    ok = r.returncode == 0
    pages = None
    m = re.search(r"완료: .*? \((\d+)개 HTML 페이지\)", r.stdout)
    if m:
        pages = int(m.group(1))
    out["build"] = (ok, pages, r.stdout[-800:] if not ok else "")
    token_ok = "확정 사실 토큰 생존 가드" in r.stdout and "이상 없음" in r.stdout
    m2 = re.search(r"확정 토큰 (\d+)건", r.stdout)
    out["tokens"] = (token_ok, int(m2.group(1)) if m2 else 0)

    t = sh([sys.executable, "build/test_validation.py"])
    tm = re.search(r"Ran (\d+) tests", t.stderr + t.stdout)
    out["tests"] = (t.returncode == 0, int(tm.group(1)) if tm else 0)

    h = sh([sys.executable, "build/hig_check.py"])
    out["hig"] = (h.returncode == 0, (h.stdout + h.stderr).strip().splitlines()[-1]
                  if (h.stdout or h.stderr) else "")
    return out


def gate3_verbatim(name):
    old = main_text(name)
    new = (CHAPTERS / name).read_text(encoding="utf-8")
    mainset = {l.strip() for l in old.splitlines() if l.strip()}
    body = [l.strip() for l in new.splitlines()
            if l.strip() and not l.strip().startswith("#")]
    miss = [l for l in body if l not in mainset]
    rate = 100 * (len(body) - len(miss)) / len(body) if body else 100.0
    return rate, miss, len(body)


def load_exceptions(name):
    """게이트 4의 명시적 예외 (사용자 확정값). 항상 로그에 노출한다."""
    import json
    path = ROOT / "docs/rs_rework/gate_exceptions.json"
    if not path.exists():
        return [], []
    data = json.loads(path.read_text(encoding="utf-8"))
    toks, notes = [], []
    for e in data.get("exceptions", []):
        if e.get("file") == name:
            toks.extend(e.get("tokens", []))
            notes.append(f"{', '.join(e.get('tokens', []))} — {e.get('reason', '')}")
    return toks, notes


def gate4_invention(name, miss):
    """미소급 행 중 사실값을 담았고, 그 사실값이 main 어디에도 없는 것."""
    old = main_text(name)
    oldn = norm(old)
    allowed, _ = load_exceptions(name)
    found = []
    for line in miss:
        for tok in set(FACT_RE.findall(line)):
            if not tok or len(tok) < 2 or tok in allowed:
                continue
            if tok not in old and norm(tok) not in oldn:
                found.append((tok, line))
    return found


def gate5_duplication(name):
    """40자 이상 본문 행이 컴펜디움에 그대로 있으면 중복 잔존."""
    if not COMPENDIUM.exists():
        return []
    comp = COMPENDIUM.read_text(encoding="utf-8")
    compset = {l.strip() for l in comp.splitlines() if len(l.strip()) >= DUP_MIN_LEN}
    new = (CHAPTERS / name).read_text(encoding="utf-8")
    dups = [l.strip() for l in new.splitlines()
            if len(l.strip()) >= DUP_MIN_LEN and l.strip() in compset]
    return dups


def gate6_polite(name):
    new = (CHAPTERS / name).read_text(encoding="utf-8")
    return [f"L{i}: {'·'.join(polite_hits(l))} — {l.strip()[:80]}"
            for i, l in enumerate(new.splitlines(), 1) if polite_hits(l)]


def reduction(name):
    old = main_text(name)
    new = (CHAPTERS / name).read_text(encoding="utf-8")
    a, b = len(reader_body(old)), len(reader_body(new))
    return a, b, 100 * (a - b) / a if a else 0.0


def run(names, build_only=False):
    print("=" * 72)
    print("게이트 1 — build · tests · hig")
    g1 = gate1_build()
    bok, pages, berr = g1["build"]
    print(f"  build.py        : {'PASS' if bok else 'FAIL'} · {pages}p")
    if berr:
        print(berr)
    tok_ok, tok_n = g1["tokens"]
    print(f"  게이트 2 토큰가드: {'PASS' if tok_ok else 'FAIL'} · 확정 토큰 {tok_n}건")
    ok, n = g1["tests"]
    print(f"  test_validation : {'PASS' if ok else 'FAIL'} · {n} tests")
    hok, hline = g1["hig"]
    print(f"  hig_check       : {'PASS' if hok else 'FAIL'} · {hline[:90]}")
    allgreen = bok and tok_ok and ok and hok
    if build_only:
        return 0 if allgreen else 1

    for name in names:
        print("=" * 72)
        print(f"[{name}]")
        a, b, red = reduction(name)
        print(f"  감량           : {a} → {b}자 ({red:.1f}%)")

        rate, miss, total = gate3_verbatim(name)
        g3 = rate >= VERBATIM_FLOOR
        print(f"  게이트 3 자구  : {'PASS' if g3 else 'FAIL'} · "
              f"{total}행 중 일치 {total - len(miss)} ({rate:.1f}%, 하한 {VERBATIM_FLOOR}%)")
        for l in miss[:12]:
            print(f"      · {l[:110]}")
        if len(miss) > 12:
            print(f"      … 외 {len(miss) - 12}행")

        inv = gate4_invention(name, miss)
        g4 = not inv
        print(f"  게이트 4 창작  : {'PASS' if g4 else 'FAIL'} · 신규 사실값 {len(inv)}건")
        for note in load_exceptions(name)[1]:
            print(f"      ※ 사용자 확정 예외: {note}")
        for tok, line in inv[:10]:
            print(f"      · '{tok}' ← {line[:90]}")

        dups = gate5_duplication(name)
        g5 = (red >= 30.0) or not dups
        print(f"  게이트 5 중복  : {'PASS' if g5 else 'FAIL'} · "
              f"컴펜디움 중복 {len(dups)}행" + ("" if red >= 30 else " (감량 30% 미달 → 0행 필요)"))
        for l in dups[:8]:
            print(f"      · {l[:110]}")

        pol = gate6_polite(name)
        g6 = not pol
        print(f"  게이트 6 경어체: {'PASS' if g6 else 'FAIL'} · {len(pol)}건")
        for l in pol[:8]:
            print(f"      · {l}")

        if not (g3 and g4 and g5 and g6):
            allgreen = False

    print("=" * 72)
    print(f"게이트 종합: {'ALL GREEN' if allgreen else 'RED'}")
    return 0 if allgreen else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--build-only", action="store_true")
    args = ap.parse_args()
    names = args.names
    if args.all:
        names = sorted(p.name for p in CHAPTERS.glob("*.md"))
    sys.exit(run(names, build_only=args.build_only))
