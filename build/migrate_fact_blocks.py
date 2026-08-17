#!/usr/bin/env python3
"""T3-3·T3-5 — 확정 등급 장소의 운영정보를 원고에서 `{{fact:}}` 블록으로 옮긴다.

**값이 없어도 블록은 만든다.** 빈 칸이 보여야 채워진다 — 정보가 없다는 사실 자체가
현장에서 알아야 할 정보다. 값이 없으면 치환기가 "미확인 — 현장 확인 필요"를 낸다.

두 서식을 쓴다.
  관광지  : 요금·운영·휴관 / 예약·소요·가는 법 (블록인용 2줄)
  식당·시장: 한 줄 (Lonely Planet 형) — 주소·가는 법·영업·휴무·예약·가격대

`--apply` 없이 돌리면 무엇을 어디에 넣을지만 보여준다.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FACTS = ROOT / "data/place-facts.json"
CH = ROOT / "source/CURRENT/20_Regional_Chapters"

REGION_PREFIX = {"barcelona": "04_", "girona": "05_", "nice": "06_", "aix": "07_",
                 "luberon": "08_", "avignon": "09_", "lyon": "10_", "paris": "11_"}

# 이름이 원고와 다른 것들. 정규식이 아니라 사람이 확인한 별칭이다.
ALIAS = {
    "le-rocher": ["Le Rocher"],
    "vieux-lyon-traboules": ["Vieux Lyon"],
    "les-halles-d-avignon": ["Les Halles"],
    "cau-ferrat": ["Cau Ferrat"],
    "museu-de-maricel": ["Museu de Maricel", "Maricel"],
    "marche-gordes": ["Gordes 화요시장", "화요시장"],
    "marche-croix-rousse": ["Croix-Rousse 시장"],
    "marche-collioure": ["콜리우르 시장"],
    "saone-rhone": ["Saône", "강변 산책"],
    "montorgueil-les-halles": ["Montorgueil"],
    "fondation-maeght": ["Fondation Maeght"],
    "grand-palais-cezanne-et-nous": ["Cezanne et nous"],
    "musee-de-l-orangerie-monet-peindre-le-temps": ["Monet, peindre le temps"],
    "a-d-aligre-butte-aux-cailles-convention-batignolles": ["월요일 모듈"],
    "placa-del-rei-carrer-del-bisbe": ["고딕지구 핵심 산책", "Plaça del Rei"],
}

# 식당·시장은 한 줄 서식을 쓴다.
EATERY_HINT = ("marche", "marché", "mercat", "market", "시장", "restaurant", "bistrot",
               "bar-", "cafe", "café", "halles", "bouillon", "fonda", "casa-", "bodega",
               "llibreria", "paradeta", "zorra", "canete", "cocottes", "fafa", "gout-",
               "ju-maison", "criquet", "fourchette", "abel", "mamie", "freti", "pipo",
               "acchiardo", "alziari", "daniel-et-denise", "sevin", "cal-ros")

SIGHT_BLOCK = (
    "> **요금** {{{{fact:{p}.price_adult}}}} · **운영** {{{{fact:{p}.hours}}}}"
    " · **휴관** {{{{fact:{p}.closed}}}}\n"
    "> **예약** {{{{fact:{p}.booking}}}} · **소요** {{{{fact:{p}.duration}}}}"
    " · **가는 법** {{{{fact:{p}.getting_there}}}}\n")

EATERY_LINE = (
    "> 📍 {{{{fact:{p}.address}}}} · 🚶 {{{{fact:{p}.getting_there}}}}"
    " · 🕐 {{{{fact:{p}.hours}}}} · 휴무 {{{{fact:{p}.closed}}}}"
    " · {{{{fact:{p}.booking}}}} · {{{{fact:{p}.price_range}}}}\n")


def is_eatery(pid, place):
    n = (pid + " " + place["displayName"]).lower()
    return any(h in n for h in EATERY_HINT)


def candidates(pid, place):
    out = list(ALIAS.get(pid, []))
    nm = place["displayName"]
    out.append(nm)
    base = re.split(r"\s*[（(]", nm)[0].strip()
    if base and base != nm:
        out.append(base)
    for sep in ("—", "·", "/"):
        if sep in base:
            out.append(base.split(sep)[0].strip())
    return [c for c in dict.fromkeys(out) if len(c) >= 3]


def find_heading(text, names):
    """이 장소의 dossier 헤딩 위치. 가장 구체적인 이름부터 찾는다."""
    for nm in sorted(names, key=len, reverse=True):
        for m in re.finditer(r"^(#{3,4})\s+(.*)$", text, re.M):
            if nm in m.group(2):
                return m
    return None


def main():
    apply = "--apply" in sys.argv
    doc = json.loads(FACTS.read_text(encoding="utf-8"))
    places = doc["places"]
    # T3-5 — 식당·시장은 등급과 무관하게 정보줄을 붙인다. 진단 기준 최악 구간이
    # 여기다 (B3 가는 법 12.5% · B5 휴무 14.8% · B4 영업시간 27.4%).
    conf = {pid: p for pid, p in places.items()
            if p.get("grade") in ("essential", "priority") or is_eatery(pid, p)}

    files = {}
    for reg, pre in REGION_PREFIX.items():
        f = next(CH.glob(pre + "*.md"), None)
        if f:
            files[reg] = f
    texts = {reg: f.read_text(encoding="utf-8") for reg, f in files.items()}

    inserted = skipped = nohead = 0
    todo = []
    for pid, p in sorted(conf.items()):
        reg = p.get("region")
        if reg not in texts:
            nohead += 1
            continue
        t = texts[reg]
        if re.search(r"\{\{fact:" + re.escape(pid) + r"\.(hours|closed|price_adult|booking)\}\}", t):
            skipped += 1          # 이미 이관된 곳
            continue
        m = find_heading(t, candidates(pid, p))
        if not m:
            nohead += 1
            todo.append((pid, reg, p["displayName"], "헤딩 없음"))
            continue
        block = (EATERY_LINE if is_eatery(pid, p) else SIGHT_BLOCK).format(p=pid)
        end = m.end()
        rest = t[end:]
        lead = re.match(r"\n+", rest)
        pos = end + (lead.end() if lead else 0)
        texts[reg] = t[:pos] + block + "\n" + t[pos:]
        inserted += 1
        todo.append((pid, reg, p["displayName"],
                     ("식당줄" if is_eatery(pid, p) else "관광블록") + f" ← {m.group(2)[:34]}"))

    if apply:
        for reg, f in files.items():
            f.write_text(texts[reg], encoding="utf-8")

    n_tok = sum(len(re.findall(r"\{\{fact:", t)) for t in texts.values())
    print(f"확정 {len(conf)}곳 · 삽입 {inserted} · 이미 있음 {skipped} · 헤딩 없음 {nohead}")
    print(f"챕터 내 {{{{fact:}}}} 토큰 수(적용 후 기준): {n_tok}")
    print("--apply 없이 미리보기" if not apply else "적용 완료")
    for pid, reg, nm, how in todo:
        if "헤딩 없음" in how:
            print(f"    ! {pid:44s} [{reg}] {nm[:32]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
