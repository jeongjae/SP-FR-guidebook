#!/usr/bin/env python3
"""업소 신원 대조 — 이름이 같은 다른 가게를 걸러 내는 한 곳.

사진을 붙일 때 가장 위험한 실수는 **이름이 비슷한 다른 업소**의 사진을
그 가게 사진처럼 쓰는 것이다. 현장에서 엉뚱한 문 앞에 서게 된다.

여기에 규칙을 모아 둔 이유는 실제로 조용히 통과한 적이 있기 때문이다.
`fold()` 는 비교를 위해 라틴 문자만 남긴다. 그런데 Google Maps 가 상호 대신
번역된 분류명을 돌려주면 — '푸에스토시요 해산물 요리' 처럼 — 접힌 결과가
**빈 문자열**이 되고, 빈 문자열은 어떤 문자열에도 들어 있으므로 부분일치
검사가 무조건 참이 된다. 그 구멍으로 La Paradeta 자리에 다른 업소
(Puertecillo) 사진이 붙을 뻔했다.

그래서 규칙은 셋이다.

    1 접힌 결과가 비면 **매치 실패**로 본다 (판단 불가는 통과가 아니다)
    2 후보 이름도 접었을 때 비면 그 후보는 버린다
    3 부분일치는 양방향으로 보되, 양쪽 모두 비어 있지 않을 때만
"""
from __future__ import annotations

import re
import unicodedata

MIN_TOKEN = 3


def fold(value: str) -> str:
    """비교용 정규화. 악센트를 벗기고 라틴 문자·숫자만 남긴다."""
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", text.lower())


def names_match(candidates, title: str) -> bool:
    """후보 상호 중 하나가 이 제목과 같은 업소를 가리키는가.

    `candidates` 는 우리가 아는 이름들(정식 상호 + 확인된 개명 이름).
    `title` 은 지도·검색이 돌려준 제목.
    """
    folded_title = fold(title)
    if len(folded_title) < MIN_TOKEN:
        # 라틴 문자가 없거나 너무 짧다 — 이름으로 판단할 수 없다.
        return False
    for candidate in candidates or []:
        folded = fold(candidate)
        if len(folded) < MIN_TOKEN:
            continue
        if folded in folded_title or folded_title in folded:
            return True
    return False
