# 상용 가이드북 개편 — 디자인 토큰 v1.0

기준: `build/assets/style.css` (라이트/다크 `:root` 2단) · 2026-08-06.
**결정 D-09: 현행 토큰을 정본화한다.** 원 지시서 §11.3 의 `--color-*` 신규 명명은
폐기 — 이미 동등 체계가 있고, 전면 개명은 위험 대비 이득이 없다.

## 1. 현행 토큰 ↔ 원 지시서 §11.3 대응

| 지시서 제안 | 현행 토큰 | 비고 |
|---|---|---|
| --color-bg / surface | `--bg` `--surface` `--surface-sunk` | |
| --color-text / muted | `--text` `--text-2` `--muted` | 본문 7:1 하한 |
| --color-accent | `--accent` `--accent-ink` `--accent-soft` | |
| --color-danger/warning/success | `--sig-critical(-ink)` `--sig-caution(-ink)` `--sig-steady` `--sig-rest` | 신호 4계열 |
| (없음) | `--acc-bcn/gir/nce/aix/lub/avn/lyo/par` | 지역 8색 |
| (없음) | `--bar-bg` `--bar-blur` `--tabbar-bg` `--border` `--separator` `--quote-bg` | 크롬 |
| (없음) | `--dur` `--ease` | 모션 |

## 2. 불변 규칙 (CLAUDE.md 승계)

1. 국기 원색은 면에만 — 금색 1.7:1 · 프랑스 빨강 3.4:1 은 글자색 금지, 글자는 `--sig-*-ink`.
2. 명암비 본문 7:1 · 보조 4.5:1 (hig_check 가 자동 검증).
3. 아이콘은 `build/icons.py` CSS 마스크 + `currentColor` — 새 팔레트 금지, 유니코드 도형 금지.
4. 다크모드는 `:root` 2단으로 유지 — 컴포넌트에 하드코딩 색 금지.

## 3. 갭 (Phase B 파일럿에서 다룰 것)

- 간격·타이포 스케일이 토큰화되어 있지 않음 (`--space-*` `--text-*` 부재). 파일럿에서
  실측 수치를 토큰으로 추출하되 **렌더 결과 불변**을 조건으로 한다 (시각 회귀 금지).
- 배지·카드 반경 등 컴포넌트 값도 동일 방식 — 값 변경 없이 이름만 부여.
