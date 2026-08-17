#!/usr/bin/env python3
"""T4-0 — 끝내 못 채운 토큰을 원고에서 지운다.

**"미확인 — 현장 확인 필요" 를 59곳에 띄우는 것보다 항목을 안 만드는 편이 낫다.**
빈 칸이 보여야 채워진다는 원칙은 편집자를 향한 것이고, 독자는 산문에 실제 값이 있는데
바로 위 블록이 "미확인"이라고 말하는 화면을 본다 — 이 인프라가 막으려던 상태다.

지우는 것은 **원고의 토큰**이지 조사 큐가 아니다. `place-facts` 레코드는 그대로 두므로
`verify-queue.csv` 는 여전히 그 항목을 조사 대상으로 센다.

`unreachable`(전화 문의 대상)은 지우지 않는다 — 그건 "모른다"가 아니라
"공식 확인 불가, 전화하라"는 **행동 지시**다.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FACTS = ROOT / "data/place-facts.json"
CH = ROOT / "source/CURRENT/20_Regional_Chapters"

KEYS = ("duration", "getting_there", "address", "price_range", "price_adult",
        "hours", "closed", "booking")


def has_value(p, key):
    f = (p.get("facts", {}) or {}).get(key) or {}
    if (f.get("value") or "").strip():
        return True
    return f.get("confidence") == "unreachable"      # 전화 문의 지시는 남긴다


def main():
    apply = "--apply" in sys.argv
    places = json.loads(FACTS.read_text(encoding="utf-8"))["places"]
    removed = {}
    for f in sorted(CH.glob("*.md")):
        text = out = f.read_text(encoding="utf-8")
        for key in KEYS:
            pat = re.compile(r"\{\{fact:([a-z0-9][a-z0-9-]*)\." + key + r"(?:\|x\d+)?\}\}")
            for pid in sorted(set(pat.findall(out))):
                p = places.get(pid)
                if p and has_value(p, key):
                    continue
                # 토큰과 그 앞의 라벨을 함께 지운다 — "· **소요** {{fact:…}}"
                out = re.sub(
                    r"\s*[·|]?\s*(?:\*\*[^*|\n]{1,12}\*\*|🕐|📍|🚶|휴무)?\s*"
                    r"\{\{fact:" + re.escape(pid) + r"\." + key + r"(?:\|x\d+)?\}\}",
                    "", out)
                removed[key] = removed.get(key, 0) + 1
        # 라벨만 남은 빈 블록 줄을 정리한다
        out = re.sub(r"^>\s*$", "", out, flags=re.M)
        out = re.sub(r"\n{3,}", "\n\n", out)
        if apply and out != text:
            f.write_text(out, encoding="utf-8")

    total = sum(removed.values())
    print(f"지운 토큰 {total}개 — " + " · ".join(f"{k} {v}" for k, v in sorted(removed.items())))
    print("--apply 없이 미리보기" if not apply else "적용 완료")
    print("※ place-facts 레코드는 그대로다 — 조사 큐는 여전히 이 항목들을 대상으로 센다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
