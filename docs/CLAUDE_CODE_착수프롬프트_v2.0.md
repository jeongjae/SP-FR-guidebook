# Claude Code 착수 프롬프트 v2.0

---

## STEP 1 — 먼저 할 일 (Jason, 5분)

다운로드한 파일 4개를 저장소에 넣고 커밋한다. **이걸 안 하면 Claude Code가 조사를 처음부터 다시 한다.**

```bash
cd <SP-FR-guidebook 로컬 경로>
git checkout main && git pull
mkdir -p docs/diagnosis-v2

# 다운로드 폴더에서 복사
cp ~/Downloads/SP-FR-guidebook_콘텐츠_전수진단_v2.0.md      docs/diagnosis-v2/
cp ~/Downloads/SP-FR-guidebook_개선계획_작업지시서_v2.0.md   docs/diagnosis-v2/
cp ~/Downloads/SP-FR_전수진단_엔트리매트릭스_v2.0.csv        docs/diagnosis-v2/
cp ~/Downloads/SP-FR_신규확정사실_v2.0.csv                  docs/diagnosis-v2/
cp ~/Downloads/SP-FR_확정사실원장_v1.0.md                   docs/diagnosis-v2/

git checkout -b docs/diagnosis-v2
git add docs/diagnosis-v2
git commit -m "docs(diagnosis): 콘텐츠 전수진단 v2.0 + 개선계획 + 확정사실 원장·매트릭스"
git push -u origin docs/diagnosis-v2
```

PR 생성 후 병합. **이 5개 파일이 저장소에 있어야 아래 프롬프트가 동작한다.**

---

## STEP 2 — Claude Code에 붙여넣을 프롬프트

아래를 **그대로** 복사해 Claude Code에 붙여넣는다.

---

```
SP-FR-guidebook 저장소에서 콘텐츠 개선 작업을 시작한다.

## 먼저 읽을 것 (순서대로, 전부)
1. docs/diagnosis-v2/SP-FR-guidebook_개선계획_작업지시서_v2.0.md  ← 실행 지시서. §0 금지사항 5가지를 먼저 읽어라
2. docs/diagnosis-v2/SP-FR_확정사실원장_v1.0.md                   ← 2026-08-16 확정값. 여기 있는 값은 절대 재조사하지 마라
3. docs/diagnosis-v2/SP-FR_신규확정사실_v2.0.csv                  ← 2026-08-17 신규 확정 75건 (소스 URL·확인일 포함)
4. docs/diagnosis-v2/SP-FR-guidebook_콘텐츠_전수진단_v2.0.md      ← 근거. §4-2(결함 22+6건)와 §5(왜 반복되는가)를 반드시 읽어라
5. docs/diagnosis-v2/SP-FR_전수진단_엔트리매트릭스_v2.0.csv        ← 315 엔트리 × 정보항목 판정. 어디가 비었는지의 정본
6. CLAUDE.md                                                      ← 저장소 규칙

## 이번 세션에서 할 일: S0만 한다
지시서 §2 (S0 — 사실 인프라 구축) 의 T0-1 ~ T0-5.
**S1(오류 수정)로 넘어가지 마라.** S0 완료 조건을 통과시키고 멈춘 뒤 보고하라.

S0 산출물:
- data/place-facts.json  (+ place-facts.schema.json)
- data/decisions.json
- build/guards/ 6종 + run_all.py
- build/ 에 {{fact:}} 치환기
- .github/workflows/pages.yml 수정

## 절대 규칙
- site/ 직접 편집 금지. main 직접 푸시 금지. 브랜치 + PR.
- 일정의 단일 진실은 source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md 와 itinerary.json 이다.
  data/itinerary-places.csv 는 전환일 4개(Day 19·23·27·43)가 밀려 있으니 날짜 근거로 쓰지 마라.
- place-facts.json 시드는 위 2·3번 파일에서만 가져온다. 웹 조사 금지 — 이번 단계는 조사 단계가 아니다.
- 공식 소스로 확인 못 한 값을 추정해 채우지 마라.
- 일정을 바꾸는 판단은 나에게 물어라.

## 완료 시 보고할 것
- place-facts.json 적재 건수 (목표 165) · confidence 분포
- 가드 6종 실행 결과 (이 시점 FAIL은 정상)
- G2가 검출한 하드코딩 건수 = baseline
- python3 build/build.py && python3 build/hig_check.py 통과 여부
- PR 링크
```

---

## STEP 3 — 이후 세션 (S0 통과 후)

같은 형식으로 단계를 하나씩 준다. **한 프롬프트에 두 단계를 넣지 마라** — 이전 세션들이 실패한 지점이다.

| 세션 | 프롬프트 핵심 | 선행 조건 |
|---|---|---|
| 2회차 | "지시서 §3 (S1) 만 실행. T1-1 → T1-2 → T1-3 → T1-4 → T1-5 → T1-6 순서. G1·G4·G5 GREEN 되면 멈춰라" | S0 병합 + **Hertz 확정 + Paris 10/1·10/6 결정** |
| 3회차 | "지시서 §4 (S2) 만 실행. verify-queue 생성 후 P0만 조사. 큐에 없는 것은 조사 금지" | S1 병합 |
| 4회차 | "지시서 §5 (S3) 만 실행. G3 GREEN + 충족률 75% 되면 멈춰라" | S2 병합 |
| 5회차 | "지시서 §7 (S5) 최종 게이트" | 8/27 |

---

## ★ Jason이 지금 해야 할 것 — S1을 막고 있다

| # | 항목 | 왜 막히나 |
|---|---|---|
| 1 | **Hertz Avignon TGV +33 4 32 74 62 80** — 9/19(토) 조기 반납 확정 | T1-2가 이걸 전제로 원고를 고친다. 미확정이면 pending 처리로 진행하되, 결국 다시 고쳐야 한다 |
| 2 | **Paris 10/1·10/6 이중 배치 결정** — 세잔전/카사트전을 도시에 절 날짜로 갈지 실행표 날짜로 갈지 | T1-1이 Day 체계를 통일하려면 어느 쪽이 정본인지 정해져야 한다 |
| 3 | **Luberon 농가 문의문 3박으로 고쳐 발송** | Claude Code와 무관. 지금 안 보내면 9월 중순 gîte 확보가 어렵다 |
| 4 | **Hertz Nice 인수지 확정** (공항 T2 vs Nice-Ville) | 공식 페이지 404로 확인 불가. 전화만 가능 |

1·2번을 먼저 답해 주면 2회차 세션이 막힘 없이 돈다.
