# Aix-en-Provence · Marseille 공공교통 — Claude Code 독립 검증 요청

## 목적

`codex/aix-transit` 브랜치의 Aix 공공교통 확장이 실제 Day 12–16 일정과 공식 교통 규칙에 맞는지 독립 검증한다. 구현자의 설명을 합격 근거로 사용하지 말고 정본 일정, 데일리 카드, 공식 출처, 빌드 산출물을 직접 대조한다. 검증 중 코드는 수정하지 않는다.

Hertz 관련 사항은 사용자가 별도로 확인할 예정이므로 이번 검증 범위에서 제외한다.

## 핵심 판정 질문

1. 현재 정본 일정이 Day 13 Aix 도보, Day 14 Cassis 차량, Day 15 Marseille TER·RTM, Day 16 Luberon 차량으로 정확히 반영됐는가?
2. 과거 원고의 `Day 14 Marseille`, `Cassis 선택 대안`, `L50 기본`, `Day 15 세잔 작업실` 편집안이 현재 안내와 충돌하지 않는가?
3. Aix 체류에서 정기권을 사지 않고 필요할 때만 비접촉 결제를 쓰는 권고가 실제 승차 횟수에 맞는가?
4. Aix en Bus의 €1.20, 한 카드 최대 5명, 매 승차·환승 검증, 첫 검증부터 1시간 규칙이 공식 페이지와 일치하는가?
5. Marseille RTM의 €1.70, 한 카드 최대 5명, bus·metro·tram 약 60분, 같은 결제수단 재검증 규칙이 공식 페이지와 일치하는가?
6. TER, Aix en Bus, RTM, L50의 적용 범위가 서로 섞이지 않는가?
7. L50 €7은 TER 장애 시 대안으로만 표시되고, 실제 Day 15 데이터에는 L50이 확정 동선으로 남지 않았는가?
8. Day 15의 RTM 60·83번과 Metro M1 연결이 데일리 카드와 지역 가이드에서 일관적인가? 미확정 구간은 확정 노선처럼 단정하지 않는가?

## 공식 출처 재검증

다음 공식 페이지를 새로 열어 현재 내용을 확인한다.

- Aix en Bus 비접촉 결제: `https://aixenbus.fr/fr/gd5-Le-paiement-sans-contact.html`
- Aix en Bus 승차·환승 규칙: `https://aixenbus.fr/fr/Pjb-Conseils-pour-bien-voyager.html`
- RTM 비접촉 결제와 L50 요금: `https://www.rtm.fr/actualites/validation-par-carte-bancaire`
- La Métropole Mobilité 노선·시간표: `https://www.lametropolemobilite.fr/plans-et-horaires/`

검색 결과 요약이나 여행 블로그를 공식 사실의 최종 근거로 쓰지 않는다. 여행일은 2026-09-09~13이므로 변경 가능성이 있으면 재확인 항목으로 분리한다.

## 데이터·화면 대조

- `data/transit-facts.json`의 `aix`
- `data/daily-cards/day-12.json`~`day-16.json`
- `source/CURRENT/20_Regional_Chapters/07_Aix_en_Provence_v2.0.md`
- `data/transit-resources.json`의 `aix`
- 빌드된 `guide/aix.html`, `daily/day-14.html`, `daily/day-15.html`

특히 Day 15 각 leg의 `mode`, `line`, 설명을 직접 대조하고 도보 leg에 교통 노선이 잘못 붙지 않았는지 확인한다.

## 실행 검사

```powershell
python -m unittest tests.test_stay_transport_guards -v
python build/site.py
python build/ux_check.py
python build/content_audit.py
python build/viewport_check.py
python build/pwa_check.py
```

모바일 390px와 데스크톱 1024px에서 Aix 지역 페이지와 Day 15를 직접 확인한다. 핵심 결론이 먼저 보이는지, 공식 링크가 열리는지, Day 12–16 링크가 맞는지, 가로 넘침·콘솔 오류가 없는지 기록한다.

## 판정 기준

- 일정·노선·요금·적용 범위의 현장 실행 오류가 있으면 `FAIL`.
- 미확정 노선을 확정처럼 안내하거나 과거 편집안이 현재 화면에 섞이면 `FAIL`.
- 핵심 사실과 화면이 일치하고 신규 회귀가 없으면 `PASS`.
- 사소한 문장 개선은 `NOTE`로 분리한다.

결과를 다음 파일에 작성한다.

`handoff/CLAUDE_CODE_AIX_TRANSIT_VERIFICATION_RESULT.md`

결과에는 검증한 커밋 해시, 공식 근거, 일정 대조표, 실행 명령 결과, 모바일 화면 결과, 최종 `PASS`/`FAIL`을 포함한다.
