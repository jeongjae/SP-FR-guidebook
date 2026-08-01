# SP-FR-guidebook 개선 인계 세트

**작성** 2026-08-01 · **출발** 2026-08-29 (D-28)

## 시작

**Claude 앱 Code 탭을 쓴다면** → `00_HANDOFF_PROMPT_CODE탭.md`
zip 하나를 GitHub 웹으로 올리고 Claude Code 에게 풀게 하는 방식이다.

**터미널·데스크톱 Claude Code 를 쓴다면** → `00_HANDOFF_PROMPT_터미널용.md`

## 구성

| 폴더 | 내용 |
|---|---|
| `00_HANDOFF_PROMPT_CODE탭.md` | **Code 탭용.** 업로드 절차 + 마일스톤별 프롬프트 |
| `00_HANDOFF_PROMPT_터미널용.md` | 터미널·데스크톱용 |
| `01_plan/` | 실행계획서(T0~T12) · 명명규칙 · 구조도 |
| `02_assets/` | style.css 드롭인 교체본 + 프리뷰 |
| `03_prototype/` | 페이지 분할 구현체 (작동함) + 프리뷰 |
| `04_content/` | Girona 보강 원고 — 문체·밀도 기준 |
| `05_evidence/` | 각 판단의 진단 근거 4건 |

## 프로토타입 실행

```bash
cd 03_prototype && python3 build.py
# → dist/chapters/girona/ 20페이지
```

의존성 없음. 브라우저로 보려면 `preview_hub.html`, `preview_place.html`.

## 핵심 3줄

1. `site/` 는 빌드 산출물이다. 직접 고치면 날아간다.
2. 미확정값을 확정처럼 표시하지 않는다.
3. 번호가 아니라 지명으로 이름을 짓는다.
