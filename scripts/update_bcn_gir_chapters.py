from pathlib import Path

# 1. Update 04_Barcelona_Sitges_v2.0.md
p_bcn = Path("source/CURRENT/20_Regional_Chapters/04_Barcelona_Sitges_v2.0.md")
content_bcn = p_bcn.read_text(encoding="utf-8")

# Add self-guides if not present
new_bcn_self_guides = """#### Bodega Joan {{grade:essential|필수}}

> **Editor's Verdict**: 1942년부터 이어진 에이샴플레의 유서 깊은 보데가. 카탈루냐 숯불 구이, 카넬로니, 해산물 빠에야의 정석.

- **체류/가격**: 75–90분 · **2인 약 €45~€70** (매일 08:00–24:00, 사전 예약 권장)
- **상세 가이드**: [Bodega Joan 전체 가이드 보기](../places/bodega-joan.html)

---
#### La Paradeta Sagrada Família {{grade:essential|필수}}

> **Editor's Verdict**: 얼음 위에 진열된 신선한 지중해 해산물을 골라 즉석에서 조리해 먹는 수산시장형 시푸드 바.

- **체류/가격**: 60–75분 · **2인 약 €35~€55** (점심 13:00–16:00, 오픈 10분 전 대기)
- **상세 가이드**: [La Paradeta Sagrada Família 전체 가이드 보기](../places/la-paradeta-sagrada-familia.html)

---
#### Bar Cañete {{grade:essential|필수}}

> **Editor's Verdict**: 라발 지구 골목의 활기찬 오픈 키친 바 카운터에서 즐기는 최상급 카탈루냐 제철 타파스.

- **체류/가격**: 75–90분 · **2인 약 €60~€90** (매일 13:00–24:00, 사전 예약 필수)
- **상세 가이드**: [Bar Cañete 전체 가이드 보기](../places/bar-canete.html)

---
#### Mercat de la Concepció {{grade:priority|우선추천}}

> **Editor's Verdict**: 1888년 모더니즘 철골 구조의 에이샴플레 대표 생활시장. 24시간 꽃시장과 신선한 제철 과일·치즈의 보고.

- **체류/입장**: 40–50분 · **무료 입장** (월–토 08:00–15:00)
- **상세 가이드**: [Mercat de la Concepció 전체 가이드 보기](../places/mercat-concepcio.html)

---
#### La Zorra {{grade:priority|우선추천}}

> **Editor's Verdict**: 시체스 해변 산책로에서 즐기는 현대적 감각의 카탈루냐 쌀요리와 아로스 아 반다(Arròs a banda).

- **체류/가격**: 75–90분 · **2인 약 €60~€85** (점심 13:00–16:30, 사전 예약 필수)
- **상세 가이드**: [La Zorra 전체 가이드 보기](../places/la-zorra.html)
"""

if "#### Bodega Joan" not in content_bcn:
    # insert before ## 음식·시장·카페·생활체험
    content_bcn = content_bcn.replace("## 음식·시장·카페·생활체험", new_bcn_self_guides + "\n---\n\n## 음식·시장·카페·생활체험")

p_bcn.write_text(content_bcn, encoding="utf-8")
print("Updated 04_Barcelona_Sitges_v2.0.md")

# 2. Update 05_Girona_Collioure_Emporda_v2.1.md
p_gir = Path("source/CURRENT/20_Regional_Chapters/05_Girona_Collioure_Emporda_v2.1.md")
content_gir = p_gir.read_text(encoding="utf-8")

new_gir_self_guides = """#### Casa Marieta {{grade:essential|필수}}

> **Editor's Verdict**: 1892년 지로나 인디펜덴시아 광장에 문을 연 역사적인 전통 식당. 마르 이 문타냐와 엠포르다 오리 요리의 정수.

- **체류/가격**: 75–90분 · **2인 약 €50~€75** (매일 13:00–16:00 / 20:00–23:00, 예약 가능)
- **상세 가이드**: [Casa Marieta 전체 가이드 보기](../places/casa-marieta.html)

---
#### Mercat del Lleó {{grade:priority|우선추천}}

> **Editor's Verdict**: 지로나 구시가지 남쪽의 활기찬 중앙 공설시장. 엠포르다 치즈, 샤퀴테리, 추쇼(Xuixo)의 보고.

- **체류/입장**: 30–45분 · **무료 입장** (월–토 07:00–14:00)
- **상세 가이드**: [Mercat del Lleó 전체 가이드 보기](../places/mercat-del-lleo.html)
"""

if "#### Casa Marieta" not in content_gir:
    content_gir = content_gir.replace("## 음식·시장·카페·생활체험", new_gir_self_guides + "\n---\n\n## 음식·시장·카페·생활체험")

p_gir.write_text(content_gir, encoding="utf-8")
print("Updated 05_Girona_Collioure_Emporda_v2.1.md")
