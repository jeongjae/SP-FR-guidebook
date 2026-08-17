#!/usr/bin/env python3
"""T3-0 — `closed` 값에서 휴무 요일을 뽑는다. 단일 구현.

**두 번의 실패를 다 피해야 한다.**

S1 판: 값 어디에 있는 요일 글자든 휴관으로 읽었다. `연중무휴 — 월–금 09:00–20:00`
       에서 월·금·토·일을 전부 휴관으로 뽑아 오탐을 냈다.
S2 판: 그 반동으로 "요일 뒤에 휴관 표현이 직접 붙은 것"만 채택했다. 그런데
       **필드 이름이 이미 `closed` 다.** `토·일` 처럼 요일만 적힌 값이 다수인데
       '휴관'이라는 단어를 한 번 더 요구해 48건을 놓쳤다.

그래서 값의 **모양**으로 판정한다. 그리고 **판정 불가를 빈 집합으로 만들지 않는다** —
UNPARSEABLE 로 따로 센다. 비어 있음이 통과로 읽히는 것이 이 프로젝트가 세 번 반복한
실패다 (G1 토큰 0 · G2 스코프 18줄 · 파서 실효 30건).
"""
import re

WD_ORDER = "월화수목금토일"
ALL_WD = set(WD_ORDER)

# 앞 글자가 한글이면 '공휴일'·'평일', 숫자면 '12월'·'25일' 의 끝글자를 요일로 오독한 것이다.
_WD = r"(?<![가-힣0-9])[월화수목금토일](?:요일)?"
_SEP = r"[·,/및\s]"
_WD_LIST = rf"{_WD}(?:{_SEP}*{_WD})*"

WD_TOKEN = re.compile(_WD)

# ① 값 전체가 요일 나열인 것. "토·일" · "월요일" · "수·목" · "월·화"
#    괄호 부기는 떼고 본다 — "화요일 (+5/1)" · "월요일 (화–일 개관)" · "화요일 (월요일 개관)"
PURE = re.compile(rf"^\s*{_WD_LIST}\s*$")

# ② 요일 뒤에 휴관 표현이 붙은 것. 복문 안에서 이것만 골라낸다.
#    "월요일 휴관" · "일요일·월요일 휴관" · "9/1~6/30 월요일 휴장" · "월요일 다수 점포 휴무"
#    사이에 짧은 수식어는 허용하되 **오전·오후는 허용하지 않는다** —
#    "매주 월요일 오전 정비 휴무" 는 그 요일에 닫는다는 뜻이 아니라 반나절 점검이다.
CLOSED_MARK = re.compile(
    rf"((?:{_WD})(?:\s*[·,및]\s*(?:{_WD}))*(?:\s*[~\-–]\s*(?:{_WD}))?)"
    r"\s*(?:은|는|만|에|엔|과|와)?\s*"
    r"(?!(?:[가-힣\s]{0,6})?(?:오전|오후))"
    r"(?:[가-힣]+\s+){0,2}"
    r"(?:정기\s*)?(?:휴관|휴무|휴장|휴점|폐관|폐장|closed)")

# ③ "그 요일에만 연다" — 나머지 전부가 휴무다.
#    "화요일 오전에만 개장" · "수요일·일요일 오전에만 선다" · "일요일 장터만 정기 개장"
ONLY_OPEN = re.compile(
    rf"((?:{_WD})(?:\s*[·,및]\s*(?:{_WD}))*)"
    r"\s*[가-힣]{0,4}\s*(?:에)?만\s*(?:정기\s*)?"
    r"(?:개장|개관|영업|운영|개방|선다|연다|열린다)")

# ④ 모른다고 적힌 값. '휴무가 없다'와 구별해야 한다 — 미확인은 빈 집합이 아니다.
UNKNOWN = re.compile(
    r"미확인|확인\s*불가|확인\s*실패|확인\s*필요|미게시|미확정|재확인|"
    r"BLOCKED|UNVERIFIED|전화로\s*직접|정보\s*없음|접근\s*실패|엇갈")

# ⑤ 정기휴무가 없다고 적힌 값.
NO_CLOSURE = re.compile(
    r"연중\s*무휴|연중\s*개방|매일\s*개(방|관|장)|매일\s*영업|상시\s*개방|상시\s*통행|"
    r"주\s*7일|7일\s*전부|365|휴무\s*없|휴관\s*없|휴장\s*없|휴무일?\s*표기\s*없|"
    r"정기\s*휴(무|관|장)일?\s*없|휴무\s*개념\s*없|시간\s*제한\s*없|"
    r"휴무일?\s*(공식\s*)?고지\s*없")

# 상태값 — 셋을 구분하는 것이 이 모듈의 존재 이유다.
PARSED = "PARSED"            # 휴무 요일을 알아냈다
NO_WEEKLY = "NO_WEEKLY"      # 주간 정기휴무가 없다고 값이 말한다
UNPARSEABLE = "UNPARSEABLE"  # 값은 있는데 판정 못 했다 ← 빈 집합으로 감추지 않는다
EMPTY = "EMPTY"              # 값이 없다 (BLOCKED 레코드). 'closed 보유'로 세지 않는다


def _expand(span):
    """'월·화' → {월,화} · '월–금' → {월,화,수,목,금}"""
    wds = [t[0] for t in WD_TOKEN.findall(span)]
    if len(wds) == 2 and re.search(r"[~\-–]", span):
        a, b = (WD_ORDER.index(w) for w in wds)
        if a <= b:
            return {WD_ORDER[i] for i in range(a, b + 1)}
    return set(wds)


def parse_closed(value):
    """returns (weekdays:set, status). status 는 위 4가지 중 하나."""
    if not value or not value.strip():
        return set(), EMPTY
    v = value.strip()
    head = re.split(r"[(（]", v)[0].strip()      # 괄호 부기는 판정에서 뺀다

    # ① 값 전체가 요일 나열이면 그대로 휴무 요일이다. 필드 이름이 이미 closed 다.
    if PURE.match(head):
        wd = _expand(head)
        if wd:
            return wd, PARSED

    # ② 복문 안의 "요일 + 휴관 표현"
    got = set()
    for m in CLOSED_MARK.finditer(v):
        got |= _expand(m.group(1))
    if got:
        return got, PARSED

    # ③ "그 요일에만 연다" → 여집합
    only = set()
    for m in ONLY_OPEN.finditer(v):
        only |= _expand(m.group(1))
    if only and only != ALL_WD:
        return ALL_WD - only, PARSED

    # ④ 모른다고 적힌 값은 '휴무 없음'이 아니다
    if UNKNOWN.search(v):
        return set(), UNPARSEABLE

    # ⑤ 정기휴무 없음
    if NO_CLOSURE.search(v):
        return set(), NO_WEEKLY

    return set(), UNPARSEABLE


# --- 보조 근거: hours 의 영업 요일 여집합 -------------------------------------
# closed 가 판정되면 closed 가 우선이다. 판정 못 했을 때만 쓴다.
HOURS_WD = re.compile(rf"{_WD}(?:\s*[~\-–]\s*{_WD})?")


def open_weekdays_from_hours(value):
    """hours 에 적힌 영업 요일의 합집합. 요일이 없으면 빈 집합."""
    if not value:
        return set()
    out = set()
    for m in HOURS_WD.finditer(value):
        out |= _expand(m.group(0))
    return out


# hours 에 요일이 적혀 있다고 나머지가 휴무인 것은 아니다. 실제 값을 보면
# "연중 매일 점심·저녁 (일·월 포함)" 의 여집합을 잡으면 정확히 거꾸로 읽는다.
# 그래서 두 조건을 다 만족할 때만 쓴다 — ① 매일·연중이라는 말이 없고
# ② 영업 요일이 범위(화–일)나 한정(수·토만)으로 **닫힌 형태**로 적혀 있다.
HOURS_EVERYDAY = re.compile(r"매일|연중|포함|무휴")
HOURS_RANGE = re.compile(rf"{_WD}\s*[~\-–]\s*{_WD}")
HOURS_ONLY = re.compile(rf"{_WD_LIST}\s*[가-힣]{{0,4}}\s*(?:에)?만")


def closed_from_hours(hours_value):
    """hours 의 영업 요일 여집합. **보조 근거이고 closed 가 있으면 closed 가 우선이다.**"""
    if not hours_value or HOURS_EVERYDAY.search(hours_value):
        return set()
    m = HOURS_ONLY.search(hours_value)
    if m:
        op = _expand(m.group(0))
    elif HOURS_RANGE.search(hours_value):
        op = open_weekdays_from_hours(hours_value)
    else:
        return set()
    return ALL_WD - op if op and op != ALL_WD else set()
