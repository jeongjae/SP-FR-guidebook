from pathlib import Path

# 1. Update 07_Aix_en_Provence_v2.0.md
p_aix = Path("source/CURRENT/20_Regional_Chapters/07_Aix_en_Provence_v2.0.md")
content_aix = p_aix.read_text(encoding="utf-8")

new_aix_self_guides = """#### Pâtisserie Weibel {{grade:essential|필수}}

> **Editor's Verdict**: 1954년부터 리셸므 시장 앞을 지켜온 엑상프로방스 대표 살롱 드 테. 정통 칼리송(Calisson)과 아침 페이스트리의 정석.

- **체류/가격**: 40–50분 · **커피 & 디저트 €8~€15** (화–일 07:30–19:00, 월 휴무)
- **상세 가이드**: [Pâtisserie Weibel 전체 가이드 보기](../places/patisserie-weibel.html)

---
#### Chez Gilbert {{grade:essential|필수}}

> **Editor's Verdict**: 카시스 구항구 앞 공인 부야베스 헌장 인증 레스토랑. 지중해 암초 생선 스튜와 카시스 AOC 화이트 와인의 정석.

- **체류/가격**: 75–90분 · **2인 약 €60~€150** (점심 12:00–14:30, 수·목 휴무, 사전 예약 필수)
- **상세 가이드**: [Chez Gilbert 전체 가이드 보기](../places/chez-gilbert-cassis.html)
"""

if "#### Pâtisserie Weibel" not in content_aix:
    content_aix = content_aix.replace("## 음식·시장·카페·생활체험", new_aix_self_guides + "\n---\n\n## 음식·시장·카페·생활체험")

p_aix.write_text(content_aix, encoding="utf-8")
print("Updated 07_Aix_en_Provence_v2.0.md")

# 2. Update 09_Avignon_Alpilles_Pont_du_Gard_v2.0.md
p_avi = Path("source/CURRENT/20_Regional_Chapters/09_Avignon_Alpilles_Pont_du_Gard_v2.0.md")
content_avi = p_avi.read_text(encoding="utf-8")

new_avi_self_guides = """#### Fou de Fafa {{grade:essential|필수}}

> **Editor's Verdict**: 탕튀리에 운하 골목에 자리한 아늑하고 로맨틱한 프로방스 모던 비스트로. 친절한 호스피탈리티와 완성도 높은 제철 코스 요리.

- **체류/가격**: 90–105분 · **3코스 1인 약 €38~€45** (저녁 18:30–21:30, 월·화 휴무, 조기 예약 필수)
- **상세 가이드**: [Fou de Fafa 전체 가이드 보기](../places/fou-de-fafa-avignon.html)

---
#### Les Cocottes Saint-Louis {{grade:essential|필수}}

> **Editor's Verdict**: 16세기 유서 깊은 수도원 회랑 안뜰 정원에서 즐기는 프랑스 무쇠 주물 냄비(Cocotte) 전통 가정식 비스트로.

- **체류/가격**: 75–90분 · **2인 약 €50~€75** (점심 12:00–14:00 / 저녁 19:00–22:00, 연중무휴)
- **상세 가이드**: [Les Cocottes Saint-Louis 전체 가이드 보기](../places/les-cocottes-saint-louis.html)

---
#### Le Gibolin {{grade:essential|필수}}

> **Editor's Verdict**: 아를 로케트 역사 지구의 활기찬 골목 비스트로. 카마르그 황소 스튜(Gardianne de taureau)와 엄선된 내추럴 와인.

- **체류/가격**: 60–75분 · **점심 코스 약 €22~€26** (점심 12:00–14:00, 일·월 휴무)
- **상세 가이드**: [Le Gibolin 전체 가이드 보기](../places/le-gibolin-arles.html)
"""

if "#### Fou de Fafa {{grade:essential|필수}}" not in content_avi:
    content_avi = content_avi.replace("## 음식·시장·카페·생활체험", new_avi_self_guides + "\n---\n\n## 음식·시장·카페·생활체험")

p_avi.write_text(content_avi, encoding="utf-8")
print("Updated 09_Avignon_Alpilles_Pont_du_Gard_v2.0.md")
