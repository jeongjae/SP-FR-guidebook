from pathlib import Path

p_paris = Path("source/CURRENT/20_Regional_Chapters/11_Paris_Long_Stay_v2.0.md")
content_paris = p_paris.read_text(encoding="utf-8")

new_paris_self_guides = """#### Boulangerie Pichard {{grade:essential|필수}}

> **Editor's Verdict**: 파리 최고의 바게트 그랑프리(Grand Prix de la Baguette) 수상에 빛나는 15구 대표 아티장 베이커리. 천연 발효 바게트 트라디시옹과 갓 구운 크루아상.

- **체류/가격**: 10–15분 · **바게트 €1.30 · 크루아상 €1.40** (수–일 07:00–20:00, 월·화 휴무)
- **상세 가이드**: [Boulangerie Pichard 전체 가이드 보기](../places/boulangerie-pichard.html)

---
#### Marché Convention {{grade:essential|필수}}

> **Editor's Verdict**: 15구 콩방시옹 대로를 따라 화·목·일 열리는 파리 서남부 최대 규모의 활기찬 정통 노천 생활시장. 제철 과일, 아티장 치즈, 로티세리 치킨의 보고.

- **체류/입장**: 30–45분 · **무료 입장** (화·목 07:00–13:30, 일 07:00–14:30)
- **상세 가이드**: [Marché Convention 전체 가이드 보기](../places/marche-convention.html)

---
#### Café du Commerce {{grade:essential|필수}}

> **Editor's Verdict**: 1921년 15구 상업거리에 문을 연 역사적인 3층 아르데코 보이드 가든 브라세리. 오리 콩피, 스테이크 프릿, 정통 에스카르고.

- **체류/가격**: 75–90분 · **2인 약 €45~€70** (매일 11:30–23:30, 연중무휴, 예약/워크인 가능)
- **상세 가이드**: [Café du Commerce 전체 가이드 보기](../places/cafe-du-commerce.html)

---
#### Le Grand Pan {{grade:essential|필수}}

> **Editor's Verdict**: 파리 15구 비스트로노미(Bistronomie)의 자존심. 셰프 브누아 고티에가 숯불로 구워내는 최상급 육류와 바스크풍 제철 미식 요리.

- **체류/가격**: 90–105분 · **1인 약 €45~€65** (월–금 12:00–14:30 / 19:30–22:30, 토·일 휴무, 사전 예약 필수)
- **상세 가이드**: [Le Grand Pan 전체 가이드 보기](../places/le-grand-pan.html)

---
#### Bouillon Chartier Montparnasse {{grade:essential|필수}}

> **Editor's Verdict**: 1903년 건립된 파리 프랑스 정부 공인 역사기념물(Monument Historique) 아르누보 식당. 전설적인 가성비 부이용.

- **체류/가격**: 60–75분 · **1인 약 €15~€22** (매일 11:30–24:00, 연중무휴, 18:30 이전 방문 권장)
- **상세 가이드**: [Bouillon Chartier Montparnasse 전체 가이드 보기](../places/bouillon-chartier-montparnasse.html)
"""

if "#### Boulangerie Pichard {{grade:essential|필수}}" not in content_paris:
    content_paris = content_paris.replace("## 음식·시장·카페·생활체험", new_paris_self_guides + "\n---\n\n## 음식·시장·카페·생활체험")

p_paris.write_text(content_paris, encoding="utf-8")
print("Updated 11_Paris_Long_Stay_v2.0.md")
