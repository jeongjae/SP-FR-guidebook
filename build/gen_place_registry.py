"""장소 레지스트리 초안을 만든다.

저장소에 흩어진 세 근거를 하나로 맞춘다.
  1) build.py 의 PLACES  — 실행지도 핀과 같은 집합 (좌표·Google Maps 의 원천)
  2) 본문의 등급 헤딩    — 보강본이 쓴 방문지 상세
  3) 본문의 추천등급 표  — 원본 원고가 매긴 등급 (Girona 는 이것만 있다)

기계로 못 가르는 것은 아래 표에 명시한다. 추측으로 채우지 않는다.
"""
import json, re, glob, unicodedata
from pathlib import Path

SLUG2REG = {'04': 'barcelona', '05': 'girona', '06': 'nice', '07': 'aix',
            '08': 'luberon', '09': 'avignon', '10': 'lyon', '11': 'paris'}
REG2SLUG = {v: k for k, v in SLUG2REG.items()}
GRADE_WORDS = {"필수": "essential", "우선 추천": "priority", "선택": "optional",
               "대체": "alternative", "비추천": "excluded"}
GRADE_KO = {v: k for k, v in GRADE_WORDS.items()}

# ── 기계로 못 가르는 것 — 근거를 달아 명시한다 ───────────────────────────
# 같은 곳인데 표기가 다른 쌍. 전부 저장소 자료로 확인했다.
ALIASES = {
    "Halles Paul Bocuse": "Halles de Lyon Paul Bocuse",     # Compendium §465
    "Parc Tête d’Or": "Parc de la Tête d'Or",               # 본문이 두 표기를 섞어 쓴다
    "Castle Hill": "Colline du Château",                    # Compendium §167
    "Libération Market": "Marché de la Libération",         # 본문 '리베라시옹 시장'
    "Atelier Cézanne": "Atelier des Lauves",                # Compendium §244 · 설명 동일
}
# 헤딩 하나에 장소가 둘 — 갈라 놓는다
SPLIT_HEADING = {"Rocher des Doms · Pont Saint-Bénézet": ["Rocher des Doms",
                                                          "Pont Saint-Bénézet"]}
# 장소가 아닌 등급 헤딩 — 하루의 성격이지 갈 곳이 아니다
NOT_A_PLACE = {"15구 생활일", "월요일 모듈"}
# 전시는 시한이 있고 장소는 남는다. 장소는 개최지다.
EXHIBITION_VENUE = {
    "Cezanne et nous — Grand Palais": "Grand Palais",
    "Mary Cassatt. L'indépendante — Musée d'Orsay": "Musée d'Orsay",
}
# 이동 기준점 — 페이지를 만들지 않고 지도·일정에서만 참조한다
NODES = {"Barcelona Sants", "Nice-Ville", "NCE T2"}
# 표기 통일 (지도 이름 → 정식 명칭)
CANON = {"Sant Pau": "Sant Pau Recinte Modernista", "Gòtic": "Barri Gòtic",
         "Uzès": "Uzès 토요시장", "Les Baux": "Les Baux-de-Provence",
         "Saint-Rémy": "Saint-Rémy-de-Provence", "Notre-Dame": "Notre-Dame de Paris",
         "Louvre": "Musée du Louvre", "Orsay": "Musée d'Orsay",
         "Montmartre": "Montmartre · South Pigalle",
         "Bourse de Commerce": "Bourse de Commerce — Pinault Collection",
         "Onyar Houses": "Onyar 강변", "Cassis": "Cassis 항구",
         "Coustellet": "Coustellet 생산자 시장", "Roussillon": "Roussillon · Sentier des Ocres",
         "Vieux Lyon": "Vieux Lyon · 트라불", "Annecy": "Annecy 구시가지",
         "Village des Bories": "Village des Bories"}

# 추천등급 표가 쓰는 변형 이름 → 장소. 원고 문구를 그대로 적어 근거를 남긴다.
TABLE_ALIAS = {
    "Cannes 당일치기": "Cannes",                    # nice: 우선 추천
    "Monaco 당일치기": "Monaco",                    # nice: 우선 추천
    "L’Isle 목요시장": "L’Isle-sur-la-Sorgue",      # luberon: 우선 추천
}
# 표가 서로 다른 등급을 매긴 것. 어느 쪽을 왜 택했는지 밝힌다.
CONFLICT_PICK = {
    ("05", "Collioure"): ("essential",
                          "요약표는 '우선 추천', 상세표(장소|등급)는 '필수'다. "
                          "상세표가 더 구체적이고 본문이 Day 5 의 축으로 다룬다."),
}
# 등급 표의 '비추천' 행 중 장소가 아니라 방식을 가리키는 것 — 등급으로 쓰지 않는다
NOT_PLACE_ROW = re.compile(r"연속 방문|중심 장기체류|3일 연속|정상 입장")

OPT_SUFFIX = re.compile(r"\s*[—–]\s*(선택|대체안|[AB]안|Day \d+ [AB]안)\s*$")


def clean(name):
    n = OPT_SUFFIX.sub("", re.sub(r"\s+", " ", name)).strip()
    n = TABLE_ALIAS.get(n, n)
    n = SPLIT_HEADING.get(n, [n])[0] if n in SPLIT_HEADING else n
    return ALIASES.get(n, CANON.get(n, n))


def slugify(name, seen):
    s = unicodedata.normalize("NFKD", name)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9가-힣]+", "-", s).strip("-").lower()
    s = s or "place"
    base, k = s, 2
    while s in seen:
        s, k = f"{base}-{k}", k + 1
    seen.add(s)
    return s


# ── 1) PLACES ─────────────────────────────────────────────────────────
src = Path("build/build.py").read_text(encoding="utf-8")
blk = re.search(r"^PLACES = \{(.*?)^\}", src, re.S | re.M).group(1)
map_names = {s: re.findall(r'^\s{8}\("([^"]+)"', b, re.M)
             for s, b in re.findall(r'^ {4}"(\d\d)": \[(.*?)^ {4}\],', blk, re.S | re.M)}

# ── 2) 등급 헤딩 ──────────────────────────────────────────────────────
graded = {}
for f in sorted(glob.glob("site/chapters/*/*.html")):
    reg = f.split("/")[2]
    if reg not in REG2SLUG:
        continue
    t = Path(f).read_text(encoding="utf-8")
    for lvl, b in re.findall(r"<h([234])[^>]*>(.*?)</h\1>", t, re.S):
        gm = re.search(r'class="grade grade-(\w+)"', b)
        if not gm:
            continue
        name = re.sub(r"<span class=\"grade.*?</span>", "", b, flags=re.S)
        name = re.sub(r"<[^>]+>", "", name).strip()
        anchor = re.search(r'id="([^"]+)"', b)
        graded.setdefault(REG2SLUG[reg], []).append(
            (name, gm.group(1), f'chapters/{reg}/{Path(f).name}'))

# ── 3) 추천등급 표 ────────────────────────────────────────────────────
table_grade = {}
for f in sorted(glob.glob("site/chapters/*/*.html")):
    reg = f.split("/")[2]
    if reg not in REG2SLUG:
        continue
    t = Path(f).read_text(encoding="utf-8")
    for row in re.findall(r"<tr>(.*?)</tr>", t, re.S):
        cells = [re.sub(r"<[^>]+>", "", c).strip()
                 for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, re.S)]
        if len(cells) < 2:
            continue
        for a, b in ((0, 1), (1, 0)):
            if cells[b] in GRADE_WORDS and cells[a] and not NOT_PLACE_ROW.search(cells[a]):
                table_grade.setdefault(REG2SLUG[reg], {}) \
                           .setdefault(clean(cells[a]), []).append(GRADE_WORDS[cells[b]])

# ── 병합 ──────────────────────────────────────────────────────────────
rows, seen_slug = [], set()
for s in sorted(SLUG2REG):
    entries = {}
    for raw, grade, page in graded.get(s, []):
        for n in SPLIT_HEADING.get(re.sub(r"\s+", " ", raw).strip(), [raw]):
            n = clean(n)
            if n in NOT_A_PLACE:
                continue
            n = EXHIBITION_VENUE.get(n, n)
            entries.setdefault(n, {})["grade"] = grade
            entries[n]["body"] = page
            entries[n]["head"] = re.sub(r"\s+", " ", raw).strip()
    for raw in map_names.get(s, []):
        n = clean(raw)
        entries.setdefault(n, {})["pin"] = raw
    for n, e in entries.items():
        if "grade" not in e:
            g = table_grade.get(s, {}).get(n) or []
            uniq = list(dict.fromkeys(g))
            if len(uniq) == 1:
                e["grade"], e["from_table"] = uniq[0], True
            elif len(uniq) > 1:
                pick = CONFLICT_PICK.get((s, n))
                if pick:
                    e["grade"], e["from_table"], e["note"] = pick[0], True, pick[1]
                else:
                    # 원고 안에서 등급이 엇갈린다. 고르지 않고 드러낸다.
                    e["conflict"] = uniq
        rows.append((s, n, e))

out = ["# 장소 레지스트리 v1.0", "",
       "가이드북의 **최소 단위**다. 갈 수 있으면 장소, 아니면 섹션이라는 기준으로 나눈다.",
       "빌드가 이 표를 읽어 장소 페이지를 만들고, 지도 핀·본문 헤딩과 대조해 어긋나면 중단한다.", "",
       "| 열 | 뜻 |", "|---|---|",
       "| **타입** | `spot` 갈 곳 · `node` 이동 기준점(역·공항, 페이지 없음) |",
       "| **등급** | 본문 등급 헤딩에서. 없으면 추천등급 표에서. 둘 다 없으면 `미정` |",
       "| **지도 핀** | 실행지도·KML 의 이름. 좌표와 Google Maps 링크의 원천 |",
       "| **본문** | 상세 서술이 있는 페이지. `—` 는 아직 서술이 없다는 뜻 |",
       "| **헤딩** | 그 페이지의 등급 헤딩 원문. 빌드가 이 문자열로 대조한다 |", ""]
n_spot = n_node = n_undecided = n_conflict = 0
for s in sorted(SLUG2REG):
    mine = [(n, e) for sl, n, e in rows if sl == s]
    out += [f"## {SLUG2REG[s]} ({s})", "",
            "| 슬러그 | 이름 | 타입 | 등급 | 지도 핀 | 본문 | 헤딩 |",
            "|---|---|---|---|---|---|---|"]
    for n, e in sorted(mine, key=lambda x: x[0]):
        typ = "node" if n in NODES else "spot"
        g = e.get("grade")
        if e.get("conflict"):
            gl = "**충돌** " + "/".join(GRADE_KO[x] for x in e["conflict"])
        else:
            gl = (GRADE_KO[g] + ("*" if e.get("from_table") else "")) if g else "미정"
        if typ == "node":
            gl, n_node = "—", n_node + 1
        else:
            n_spot += 1
            if not g:
                n_undecided += 1
                if e.get("conflict"):
                    n_conflict += 1
        out.append(f"| `{slugify(n, seen_slug)}` | {n} | {typ} | {gl} | "
                   f"{e.get('pin', '—')} | {e.get('body', '—')} | {e.get('head', '—')} |")
    out.append("")
out += ["---", "",
        f"**spot {n_spot} · node {n_node} · 등급 미정 {n_undecided}"
        f"(그중 원고 충돌 {n_conflict})**", "",
        "`*` 는 등급을 본문 헤딩이 아니라 추천등급 표에서 가져왔다는 표시다.", "",
        "## 판단이 들어간 곳", "",
        "기계로 못 가른 것과 그 근거다.", ""]
out += [f"- **{n}** — {e['note']}" for _s, n, e in rows if e.get("note")]
out += ["- **Rotonde · Bellecour** — 등급 미정으로 둔다. 원고가 `Presqu’île·Bellecour·Jacobins`",
        "  라는 권역에만 등급을 매겼고 광장 단독 등급이 아니다. Rotonde 는 근거가 없다.",
        "- **역·공항 3곳** — `node` 로 두고 장소 페이지를 만들지 않는다. 지도와 일정에서만 참조한다.",
        "- **`15구 생활일` · `월요일 모듈`** — 등급이 붙어 있지만 하루의 성격이지 갈 곳이 아니다. 뺐다.",
        "- **전시 헤딩 2건** — 전시는 시한이 있고 장소는 남는다. Grand Palais · Musée d’Orsay 로 접었다.",
        "- **`Rocher des Doms · Pont Saint-Bénézet`** — 헤딩 하나에 장소가 둘이라 갈랐다.", ""]
Path("source/ASSETS/91_Place_Registry_v1.0.md").write_text("\n".join(out), encoding="utf-8")
print(f"spot {n_spot} · node {n_node} · 미정 {n_undecided} (충돌 {n_conflict})")
