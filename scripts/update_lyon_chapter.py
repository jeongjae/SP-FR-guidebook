from pathlib import Path

p_lyon = Path("source/CURRENT/20_Regional_Chapters/10_Lyon_v2.0.md")
content_lyon = p_lyon.read_text(encoding="utf-8")

new_lyon_self_guides = """#### Café Comptoir Abel {{grade:essential|필수}}

> **Editor's Verdict**: 1726년부터 에네(Ainay) 지구를 지켜온 리옹에서 가장 오래된 유서 깊은 부숑. 전통 끄넬(Quenelle de brochet)과 크림 치킨의 원형.

- **체류/가격**: 75–90분 · **3코스 1인 약 €38~€48** (매일 12:00–14:00 / 19:30–22:00, 사전 예약 필수)
- **상세 가이드**: [Café Comptoir Abel 전체 가이드 보기](../places/cafe-comptoir-abel.html)

---
#### Daniel et Denise {{grade:essential|필수}}

> **Editor's Verdict**: 프랑스 최고 장인(MOF) 조제프 비올라 셰프가 이끄는 '진짜 리옹 부숑' 공인 대표 레스토랑. 세계 챔피언 파테 앙 크루트.

- **체류/가격**: 75–90분 · **3코스 1인 약 €39~€46** (월–금 12:00–14:00 / 19:30–22:00, 토·일 휴무, 사전 예약 필수)
- **상세 가이드**: [Daniel et Denise 전체 가이드 보기](../places/daniel-et-denise.html)

---
#### Chez Mamie Lise {{grade:essential|필수}}

> **Editor's Verdict**: 안시 구시가지 운하 골목의 유서 깊은 알프스 전통 목조 산장(Chalet) 식당. 사부아 치즈 퐁뒤와 타르티플레트, 호수 생선.

- **체류/가격**: 60–75분 · **단품/세트 €18~€26** (매일 12:00–14:00 / 19:00–22:00, 사전 예약 권장)
- **상세 가이드**: [Chez Mamie Lise 전체 가이드 보기](../places/chez-mamie-lise.html)
"""

if "#### Café Comptoir Abel {{grade:essential|필수}}" not in content_lyon:
    content_lyon = content_lyon.replace("## 음식·시장·카페·생활체험", new_lyon_self_guides + "\n---\n\n## 음식·시장·카페·생활체험")

p_lyon.write_text(content_lyon, encoding="utf-8")
print("Updated 10_Lyon_v2.0.md")
