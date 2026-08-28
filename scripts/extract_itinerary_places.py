#!/usr/bin/env python3
"""Build the 43-day place inventory from the current master itinerary.

The Markdown itinerary remains the authority for dates, bases and themes.  The
curated place references below normalize names and distinguish actual stops from
optional and reference-only alternatives; they deliberately contain no private
address, coordinates or accommodation exterior.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "source/CURRENT/10_Core/03_Whole_Trip_Master_Itinerary_v1.2.md"
AUDIT = ROOT / "source/OPERATIONS/100_Whole_Trip_43_Day_Execution_Audit_v1.0.md"
OUTPUT_JSON = ROOT / "data/itinerary-places.json"
OUTPUT_CSV = ROOT / "data/itinerary-places.csv"
TRIP_START = date(2026, 8, 29)
REGIONAL = {
    "barcelona": "source/CURRENT/20_Regional_Chapters/04_Barcelona_Sitges_v2.0.md",
    "girona": "source/CURRENT/20_Regional_Chapters/05_Girona_Collioure_Emporda_v2.1.md",
    "nice": "source/CURRENT/20_Regional_Chapters/06_Nice_Cote_d_Azur_v2.0.md",
    "verdon": "source/CURRENT/20_Regional_Chapters/06B_Verdon_Moustiers_v1.0.md",
    "aix": "source/CURRENT/20_Regional_Chapters/07_Aix_en_Provence_v2.0.md",
    "luberon": "source/CURRENT/20_Regional_Chapters/08_Luberon_Farmhouse_v2.0.md",
    "avignon": "source/CURRENT/20_Regional_Chapters/09_Avignon_Alpilles_Pont_du_Gard_v2.0.md",
    "lyon": "source/CURRENT/20_Regional_Chapters/10_Lyon_v2.0.md",
    "paris": "source/CURRENT/20_Regional_Chapters/11_Paris_Long_Stay_v2.0.md",
}


@dataclass(frozen=True)
class Place:
    name: str
    name_ko: str
    place_type: str
    chapter: str
    importance: str = "supporting"
    photo_needed: bool = True
    visibility: str = "public"


def p(name, ko, kind, chapter, importance="supporting", photo=True, visibility="public"):
    return Place(name, ko, kind, chapter, importance, photo, visibility)


# One normalized identity per reusable place. Generic activities and unnamed
# private stays are included only when they materially explain a day.
PLACES = {
    "barcelona": p("Barcelona", "바르셀로나", "city", "barcelona", "hero"),
    "barcelona-airport": p("Barcelona–El Prat Airport", "바르셀로나 엘프라트 공항", "airport", "barcelona", "text-only", False),
    "eixample": p("Eixample", "에이샴플라", "neighborhood", "barcelona", "major"),
    "sagrada-familia": p("Basílica de la Sagrada Família", "사그라다 파밀리아", "attraction", "barcelona", "hero"),
    "avinguda-de-gaudi": p("Avinguda de Gaudí", "가우디 거리", "street", "barcelona", "supporting"),
    "sant-pau-recinte-modernista": p("Recinte Modernista de Sant Pau", "산 파우 모더니즘 지구", "attraction", "barcelona", "major"),
    "gracia": p("Vila de Gràcia", "그라시아", "neighborhood", "barcelona", "supporting"),
    "mercat-de-la-concepcio": p("Mercat de la Concepció", "콘셉시오 시장", "market", "barcelona", "major"),
    "barri-gotic": p("Barri Gòtic", "고딕 지구", "neighborhood", "barcelona", "hero"),
    "biblioteca-de-catalunya": p("Biblioteca de Catalunya", "카탈루냐 도서관", "library", "barcelona", "major"),
    "macba": p("Museu d’Art Contemporani de Barcelona (MACBA)", "바르셀로나 현대미술관", "museum", "barcelona", "major"),
    "llibreria-finestres": p("Llibreria Finestres", "피네스트레스 서점", "bookshop", "barcelona", "supporting", False),
    "barcelona-sants": p("Barcelona Sants", "바르셀로나 산츠역", "station", "barcelona", "text-only", False),
    "sitges": p("Sitges", "시체스", "town", "barcelona", "hero"),
    "cau-ferrat": p("Museu del Cau Ferrat", "카우 페라트 미술관", "museum", "barcelona", "major"),
    "palau-de-maricel": p("Palau de Maricel", "마리셀 궁전", "attraction", "barcelona", "major"),
    "pa-amb-tomaquet": p("Pa amb tomàquet", "파 암 토마켓", "food", "barcelona", "supporting"),
    "crema-catalana": p("Crema catalana", "크레마 카탈라나", "food", "barcelona", "supporting"),
    "bascara": p("Bàscara", "바스카라", "town", "girona", "supporting"),
    "bascara-private-stay": p("Bàscara private stay", "바스카라 비공개 숙소", "accommodation", "girona", "text-only", False, "private"),
    "girona": p("Girona", "지로나", "city", "girona", "hero"),
    "collioure": p("Collioure", "콜리우르", "town", "girona", "hero"),
    "cadaques": p("Cadaqués", "카다케스", "town", "girona", "hero"),
    "tossa-de-mar": p("Tossa de Mar", "토사 데 마르", "town", "girona", "major"),
    "sant-feliu-de-guixols": p("Sant Feliu de Guíxols", "산트 펠리우 데 기솔스", "town", "girona", "major"),
    "pals": p("Pals", "팔스", "village", "girona", "supporting"),
    "peratallada": p("Peratallada", "페라탈랴다", "village", "girona", "major"),
    "nice": p("Nice", "니스", "city", "nice", "hero"),
    "cours-saleya": p("Cours Saleya", "쿠르 살레야 시장", "market", "nice", "major"),
    "vieux-nice": p("Vieux Nice", "니스 구시가지", "neighborhood", "nice", "hero"),
    "colline-du-chateau": p("Colline du Château", "니스 성채 언덕", "viewpoint", "nice", "major"),
    "port-de-nice": p("Port de Nice", "니스 항구", "harbor", "nice"),
    "nice-beach": p("Nice seafront", "니스 해변", "beach", "nice"),
    "cannes": p("Cannes", "칸", "city", "nice", "hero"),
    "marche-forville": p("Marché Forville", "포르빌 시장", "market", "nice", "major"),
    "le-suquet": p("Le Suquet", "르 쉬케 구시가지", "neighborhood", "nice", "major"),
    "vieux-port-cannes": p("Vieux-Port de Cannes", "칸 구항", "harbor", "nice"),
    "croisette": p("Boulevard de la Croisette", "크루아제트 대로", "street", "nice", "major"),
    "monaco": p("Monaco", "모나코", "city", "nice", "hero"),
    "monaco-ville": p("Monaco-Ville", "모나코빌 구시가지", "neighborhood", "nice", "major"),
    "place-du-palais": p("Place du Palais", "모나코 궁전 광장", "square", "nice", "major"),
    "monaco-cathedral": p("Cathédrale de Monaco", "모나코 대성당", "attraction", "nice", "major"),
    "port-hercule": p("Port Hercule", "에르퀼 항구", "harbor", "nice"),
    "monte-carlo": p("Monte-Carlo", "몬테카를로", "neighborhood", "nice", "major"),
    "japanese-garden-monaco": p("Japanese Garden Monaco", "모나코 일본정원", "garden", "nice"),
    "larvotto": p("Larvotto", "라르보토 해변", "beach", "nice"),
    "marche-de-la-liberation": p("Marché de la Libération", "리베라시옹 시장", "market", "nice", "major"),
    "musee-photographie-charles-negre": p("Musée de la Photographie Charles Nègre", "샤를 네그르 사진미술관", "museum", "nice", "supporting"),
    "promenade-des-anglais": p("Promenade des Anglais", "영국인 산책로", "promenade", "nice", "hero"),
    "nice-airport-t2": p("Nice Côte d’Azur Airport Terminal 2", "니스 공항 제2터미널", "airport", "nice", "text-only", False),
    "moustiers-sainte-marie": p("Moustiers-Sainte-Marie", "무스티에생트마리", "village", "verdon", "hero"),
    "point-sublime": p("Point Sublime", "푸앵 쉬블림", "viewpoint", "verdon", "major"),
    "route-des-cretes": p("Route des Crêtes (D23)", "루트 데 크레트", "nature", "verdon", "major"),
    "lac-de-sainte-croix": p("Lac de Sainte-Croix (Pont du Galetas)", "생트크루아 호수", "nature", "verdon", "major"),
    "plateau-de-valensole": p("Plateau de Valensole", "발랑솔 고원", "nature", "verdon", "supporting"),
    "castellane": p("Castellane", "카스텔란", "town", "verdon", "supporting", False),
    "saint-paul-de-vence": p("Saint-Paul-de-Vence", "생폴드방스", "village", "aix", "major"),
    "grasse": p("Grasse", "그라스", "town", "aix", "major"),
    "aix-en-provence": p("Aix-en-Provence", "엑상프로방스", "city", "aix", "hero"),
    "aix-markets": p("Aix-en-Provence markets", "엑상프로방스 시장", "market", "aix", "major"),
    "cours-mirabeau": p("Cours Mirabeau", "미라보 거리", "street", "aix", "hero"),
    "musee-granet": p("Musée Granet", "그라네 미술관", "museum", "aix", "major"),
    "quartier-mazarin": p("Quartier Mazarin", "마자랭 지구", "neighborhood", "aix"),
    "aix-cathedral": p("Cathédrale Saint-Sauveur", "생소뵈르 대성당", "attraction", "aix"),
    "cassis": p("Cassis", "카시스", "town", "aix", "hero"),
    "calanques": p("Calanques National Park", "칼랑크 국립공원", "nature", "aix", "major"),
    "marseille": p("Marseille", "마르세유", "city", "aix", "supporting"),
    "mucem": p("Mucem", "유럽지중해문명박물관", "museum", "aix", "supporting"),
    "atelier-des-lauves": p("Atelier de Cézanne", "세잔 아틀리에", "museum", "aix", "major"),
    "lourmarin": p("Lourmarin", "루르마랭", "village", "luberon", "hero"),
    "coustellet": p("Coustellet", "쿠스텔레", "village", "luberon"),
    "luberon": p("Luberon", "뤼베롱", "region", "luberon", "hero"),
    "luberon-private-stay": p("Luberon private farmhouse", "뤼베롱 비공개 농가 숙소", "accommodation", "luberon", "text-only", False, "private"),
    "roussillon": p("Roussillon", "루시용", "village", "luberon", "hero"),
    "sentier-des-ocres": p("Sentier des Ocres", "오커 산책로", "trail", "luberon", "major"),
    "goult": p("Goult", "굴트", "village", "luberon", "supporting"),
    "bonnieux": p("Bonnieux", "보니외", "village", "luberon", "supporting"),
    "lacoste": p("Lacoste", "라코스트", "village", "luberon", "supporting"),
    "gordes": p("Gordes", "고르드", "village", "luberon", "hero"),
    "village-des-bories": p("Village des Bories", "보리 석조마을", "historic-site", "luberon", "major"),
    "abbaye-de-senanque": p("Abbaye Notre-Dame de Sénanque", "세낭크 수도원", "attraction", "luberon", "major"),
    "menerbes": p("Ménerbes", "메네르브", "village", "luberon", "supporting"),
    "oppede-le-vieux": p("Oppède-le-Vieux", "오페드 르 비외", "village", "luberon", "supporting"),
    "l-isle-sur-la-sorgue": p("L’Isle-sur-la-Sorgue", "릴쉬르라소르그", "town", "luberon", "hero"),
    "fontaine-de-vaucluse": p("Fontaine-de-Vaucluse", "퐁텐드보클뤼즈", "village", "luberon", "supporting"),
    "avignon": p("Avignon", "아비뇽", "city", "avignon", "hero"),
    "les-halles-avignon": p("Les Halles d’Avignon", "아비뇽 레 알 시장", "market", "avignon", "major"),
    "palais-des-papes": p("Palais des Papes", "교황청 궁전", "palace", "avignon", "hero"),
    "rocher-des-doms": p("Rocher des Doms", "로셰 데 돔", "garden", "avignon", "major"),
    "pont-saint-benezet": p("Pont Saint-Bénézet", "생 베네제 다리", "historic-site", "avignon", "major"),
    "uzes": p("Uzès", "위제스", "town", "avignon", "hero"),
    "pont-du-gard": p("Pont du Gard", "퐁 뒤 가르", "historic-site", "avignon", "hero"),
    "nimes": p("Nîmes", "님", "city", "avignon", "major"),
    "arenes-de-nimes": p("Arènes de Nîmes", "님 원형경기장", "historic-site", "avignon", "major"),
    "maison-carree": p("Maison Carrée", "메종 카레", "historic-site", "avignon", "major"),
    "arles": p("Arles", "아를", "city", "avignon", "hero"),
    "arenes-d-arles": p("Arènes d’Arles", "아를 원형경기장", "historic-site", "avignon", "major"),
    "theatre-antique-arles": p("Théâtre antique d’Arles", "아를 고대극장", "historic-site", "avignon", "major"),
    "place-du-forum-arles": p("Place du Forum", "포룸 광장", "square", "avignon", "supporting"),
    "cloitre-saint-trophime": p("Cloître Saint-Trophime", "생트로핌 회랑", "historic-site", "avignon", "major"),
    "la-roquette": p("La Roquette", "라 로케트", "neighborhood", "avignon", "supporting"),
    "les-baux-de-provence": p("Les Baux-de-Provence", "레 보 드 프로방스", "village", "avignon", "hero"),
    "saint-remy-de-provence": p("Saint-Rémy-de-Provence", "생레미드프로방스", "town", "avignon", "major"),
    "orange": p("Orange", "오랑주", "city", "avignon", "supporting"),
    "glanum": p("Glanum", "글라눔", "historic-site", "avignon", "supporting"),
    "carrieres-des-lumieres": p("Carrières des Lumières", "카리에르 드 뤼미에르", "attraction", "avignon", "supporting"),
    "avignon-tgv": p("Avignon TGV", "아비뇽 TGV역", "station", "avignon", "text-only", False),
    "lyon": p("Lyon", "리옹", "city", "lyon", "hero"),
    "ainay": p("Ainay", "에네 지구", "neighborhood", "lyon"),
    "place-bellecour": p("Place Bellecour", "벨쿠르 광장", "square", "lyon", "major"),
    "place-des-jacobins": p("Place des Jacobins", "자코뱅 광장", "square", "lyon"),
    "saone": p("Saône riverfront", "손강변", "riverfront", "lyon"),
    "fourviere": p("Fourvière", "푸르비에르", "attraction", "lyon", "hero"),
    "vieux-lyon": p("Vieux Lyon", "리옹 구시가지", "neighborhood", "lyon", "major"),
    "cathedrale-saint-jean-lyon": p("Cathédrale Saint-Jean-Baptiste", "리옹 생장 대성당", "attraction", "lyon", "major"),
    "traboules": p("Vieux Lyon traboules", "리옹 트라불", "historic-site", "lyon", "major"),
    "roman-theatres-lyon": p("Ancient Theatre of Fourvière", "푸르비에르 로마극장", "historic-site", "lyon"),
    "croix-rousse": p("Croix-Rousse", "크루아루스", "neighborhood", "lyon", "major"),
    "halles-de-lyon-paul-bocuse": p("Halles de Lyon Paul Bocuse", "폴 보퀴즈 시장", "market", "lyon", "major"),
    "parc-de-la-tete-d-or": p("Parc de la Tête d’Or", "테트 도르 공원", "park", "lyon", "supporting"),
    "annecy": p("Annecy", "안시", "town", "lyon", "hero"),
    "annecy-vieille-ville": p("Vieille Ville d’Annecy", "안시 구시가지", "neighborhood", "lyon", "major"),
    "thiou": p("Thiou", "티우 운하", "canal", "lyon", "major"),
    "lake-annecy": p("Lake Annecy", "안시 호수", "lake", "lyon", "hero"),
    "lyon-part-dieu": p("Lyon Part-Dieu", "리옹 파르디외역", "station", "lyon", "text-only", False),
    "paris": p("Paris", "파리", "city", "paris", "hero"),
    "gare-de-lyon-paris": p("Gare de Lyon", "파리 리옹역", "station", "paris", "text-only", False),
    "latin-quarter": p("Latin Quarter", "라탱 지구", "neighborhood", "paris", "hero"),
    "notre-dame-de-paris": p("Notre-Dame de Paris", "노트르담 대성당", "attraction", "paris", "hero"),
    "ile-saint-louis": p("Île Saint-Louis", "생루이섬", "neighborhood", "paris"),
    "pantheon-paris": p("Panthéon", "팡테옹", "historic-site", "paris", "major"),
    "jardin-du-luxembourg": p("Jardin du Luxembourg", "뤽상부르 공원", "park", "paris", "major"),
    "marche-monge": p("Marché Monge", "몽주 시장", "market", "paris", "major"),
    "le-marais": p("Le Marais", "마레 지구", "neighborhood", "paris", "hero"),
    "musee-du-louvre": p("Musée du Louvre", "루브르 박물관", "museum", "paris", "hero"),
    "palais-royal": p("Palais-Royal", "팔레 루아얄", "palace", "paris", "major"),
    "montmartre": p("Montmartre", "몽마르트르", "neighborhood", "paris", "hero"),
    "sacre-coeur": p("Basilique du Sacré-Cœur", "사크레쾨르 대성당", "attraction", "paris", "major"),
    "abbesses": p("Abbesses", "아베스", "neighborhood", "paris"),
    "south-pigalle": p("South Pigalle", "사우스 피갈", "neighborhood", "paris"),
    "bnf-richelieu": p("BnF Richelieu", "프랑스 국립도서관 리슐리외", "library", "paris", "major"),
    "passages-couverts": p("Passages couverts", "파리 아케이드", "promenade", "paris", "major"),
    "philharmonie-de-paris": p("Philharmonie de Paris", "파리 필하모니", "performance-venue", "paris", "major"),
    "grand-palais": p("Grand Palais", "그랑 팔레", "museum", "paris", "hero"),
    "marche-des-enfants-rouges": p("Marché des Enfants Rouges", "앙팡 루주 시장", "market", "paris", "major"),
    "versailles": p("Palace of Versailles", "베르사유 궁전", "palace", "paris", "hero"),
    "versailles-gardens": p("Gardens of Versailles", "베르사유 정원", "garden", "paris", "major"),
    "trianon": p("Grand and Petit Trianon", "트리아농", "palace", "paris", "major"),
    "paris-15e": p("15th arrondissement of Paris", "파리 15구", "neighborhood", "paris", "supporting"),
    "canal-saint-martin": p("Canal Saint-Martin", "생마르탱 운하", "canal", "paris", "major"),
    "paris-east-south-neighborhoods": p("Eastern and southern Paris neighborhoods", "파리 동부·남부 생활권", "neighborhood", "paris", "supporting"),
    "musee-d-orsay": p("Musée d’Orsay", "오르세 미술관", "museum", "paris", "hero"),
    "seine": p("Seine riverfront", "센강변", "riverfront", "paris", "major"),
    "bourse-de-commerce": p("Bourse de Commerce — Pinault Collection", "부르스 드 코메르스", "museum", "paris", "hero"),
    "montorgueil": p("Rue Montorgueil", "몽토르게유 거리", "street", "paris", "major"),
    "giverny": p("Giverny", "지베르니", "village", "paris", "hero"),
    "musee-de-l-orangerie": p("Musée de l’Orangerie", "오랑주리 미술관", "museum", "paris", "major"),
    "jardin-des-tuileries": p("Jardin des Tuileries", "튈르리 정원", "garden", "paris", "major"),
    "fondation-louis-vuitton": p("Fondation Louis Vuitton", "루이비통 재단 미술관", "museum", "paris", "major"),
    "charles-de-gaulle-airport": p("Paris Charles de Gaulle Airport", "파리 샤를 드골 공항", "airport", "paris", "text-only", False),
}


# (place id, status). Core stops are confirmed; conditional/deletion levers are
# optional; replacement-only locations are reference. The day-level hero is the
# first public photo-needed item with hero importance.
DAY_REFS = {
    1: [("barcelona-airport", "confirmed"), ("barcelona", "confirmed"), ("eixample", "optional")],
    2: [("barcelona", "confirmed"), ("sagrada-familia", "confirmed"), ("avinguda-de-gaudi", "confirmed"), ("sant-pau-recinte-modernista", "confirmed"), ("gracia", "optional"), ("pa-amb-tomaquet", "reference")],
    3: [("barcelona", "confirmed"), ("mercat-de-la-concepcio", "confirmed"), ("barri-gotic", "confirmed"), ("biblioteca-de-catalunya", "confirmed"), ("macba", "confirmed"), ("llibreria-finestres", "optional"), ("crema-catalana", "reference")],
    4: [("barcelona-sants", "confirmed"), ("sitges", "confirmed"), ("cau-ferrat", "optional"), ("palau-de-maricel", "optional"), ("bascara", "confirmed"), ("bascara-private-stay", "private"), ("girona", "optional")],
    5: [("bascara-private-stay", "private"), ("collioure", "confirmed"), ("cadaques", "confirmed")],
    6: [("bascara-private-stay", "private"), ("tossa-de-mar", "confirmed"), ("sant-feliu-de-guixols", "confirmed"), ("pals", "optional"), ("peratallada", "confirmed")],
    7: [("bascara-private-stay", "private"), ("nice", "confirmed")],
    8: [("nice", "confirmed"), ("cours-saleya", "confirmed"), ("vieux-nice", "confirmed"), ("colline-du-chateau", "confirmed"), ("port-de-nice", "optional"), ("nice-beach", "optional")],
    9: [("cannes", "confirmed"), ("marche-forville", "confirmed"), ("le-suquet", "confirmed"), ("vieux-port-cannes", "confirmed"), ("croisette", "confirmed")],
    10: [("monaco", "confirmed"), ("monaco-ville", "confirmed"), ("place-du-palais", "confirmed"), ("monaco-cathedral", "confirmed"), ("port-hercule", "confirmed"), ("monte-carlo", "confirmed"), ("japanese-garden-monaco", "optional"), ("larvotto", "optional")],
    11: [("nice", "confirmed"), ("marche-de-la-liberation", "confirmed"), ("musee-photographie-charles-negre", "optional"), ("promenade-des-anglais", "optional")],
    12: [("saint-paul-de-vence", "confirmed"), ("grasse", "optional"), ("castellane", "optional"), ("point-sublime", "confirmed"), ("moustiers-sainte-marie", "confirmed")],
    13: [("moustiers-sainte-marie", "confirmed"), ("route-des-cretes", "confirmed"), ("lac-de-sainte-croix", "confirmed"), ("plateau-de-valensole", "optional"), ("aix-en-provence", "confirmed")],
    14: [("marseille", "confirmed"), ("mucem", "confirmed")],
    15: [("aix-en-provence", "confirmed"), ("aix-markets", "confirmed"), ("cours-mirabeau", "confirmed"), ("musee-granet", "confirmed"), ("atelier-des-lauves", "confirmed"), ("quartier-mazarin", "confirmed"), ("aix-cathedral", "optional")],
    16: [("cassis", "confirmed"), ("calanques", "confirmed")],
    17: [("lourmarin", "confirmed"), ("lacoste", "confirmed"), ("bonnieux", "optional"), ("gordes", "confirmed")],
    18: [("gordes", "confirmed"), ("roussillon", "confirmed"), ("sentier-des-ocres", "confirmed"), ("abbaye-de-senanque", "confirmed"), ("l-isle-sur-la-sorgue", "optional")],
    19: [("saint-remy-de-provence", "confirmed"), ("les-baux-de-provence", "confirmed"), ("avignon", "confirmed")],
    20: [("uzes", "confirmed"), ("pont-du-gard", "confirmed"), ("nimes", "confirmed"), ("arenes-de-nimes", "confirmed"), ("maison-carree", "confirmed"), ("avignon-tgv", "confirmed")],
    21: [("arles", "confirmed"), ("arenes-d-arles", "confirmed"), ("theatre-antique-arles", "confirmed"), ("place-du-forum-arles", "confirmed"), ("cloitre-saint-trophime", "confirmed"), ("la-roquette", "confirmed")],
    22: [("les-halles-avignon", "confirmed"), ("palais-des-papes", "confirmed"), ("rocher-des-doms", "confirmed"), ("pont-saint-benezet", "confirmed")],
    23: [("avignon-tgv", "confirmed"), ("lyon-part-dieu", "confirmed"), ("lyon", "confirmed"), ("place-bellecour", "confirmed"), ("place-des-jacobins", "optional"), ("saone", "optional")],
    24: [("avignon-tgv", "confirmed"), ("lyon", "confirmed"), ("ainay", "confirmed"), ("place-bellecour", "confirmed"), ("place-des-jacobins", "optional"), ("saone", "optional")],
    25: [("fourviere", "confirmed"), ("vieux-lyon", "confirmed"), ("cathedrale-saint-jean-lyon", "confirmed"), ("traboules", "confirmed"), ("roman-theatres-lyon", "optional")],
    26: [("croix-rousse", "confirmed"), ("halles-de-lyon-paul-bocuse", "confirmed"), ("parc-de-la-tete-d-or", "optional")],
    27: [("annecy", "confirmed"), ("annecy-vieille-ville", "confirmed"), ("thiou", "confirmed"), ("lake-annecy", "confirmed")],
    28: [("lyon-part-dieu", "confirmed"), ("paris", "confirmed"), ("gare-de-lyon-paris", "confirmed")],
    29: [("latin-quarter", "confirmed"), ("notre-dame-de-paris", "confirmed"), ("ile-saint-louis", "confirmed"), ("pantheon-paris", "optional")],
    30: [("jardin-du-luxembourg", "confirmed"), ("marche-monge", "confirmed"), ("le-marais", "confirmed")],
    31: [("musee-du-louvre", "confirmed"), ("palais-royal", "optional")],
    32: [("montmartre", "confirmed"), ("sacre-coeur", "confirmed"), ("abbesses", "confirmed"), ("south-pigalle", "confirmed")],
    33: [("bnf-richelieu", "confirmed"), ("passages-couverts", "confirmed"), ("philharmonie-de-paris", "confirmed")],
    34: [("grand-palais", "confirmed")],
    35: [("marche-des-enfants-rouges", "confirmed"), ("le-marais", "confirmed")],
    36: [("versailles", "optional"), ("versailles-gardens", "optional"), ("trianon", "optional"), ("paris-15e", "reference")],
    37: [("canal-saint-martin", "optional")],
    38: [("paris-east-south-neighborhoods", "optional")],
    39: [("seine", "confirmed"), ("musee-d-orsay", "confirmed")],
    40: [("bourse-de-commerce", "confirmed"), ("montorgueil", "confirmed")],
    41: [("giverny", "optional"), ("musee-de-l-orangerie", "reference"), ("jardin-des-tuileries", "reference")],
    42: [("paris", "confirmed"), ("fondation-louis-vuitton", "optional")],
    43: [("paris", "confirmed"), ("charles-de-gaulle-airport", "confirmed")],
}


def parse_master():
    rows = []
    for line in MASTER.read_text(encoding="utf-8").splitlines():
        if not re.match(r"^\|\s*\d+\s*\|", line):
            continue
        cells = [re.sub(r"\*\*", "", c.strip()) for c in line.strip().strip("|").split("|")]
        if len(cells) != 8:
            continue
        day = int(cells[0])
        d = TRIP_START.fromordinal(TRIP_START.toordinal() + day - 1)
        rows.append({
            "day": day, "date": d.isoformat(), "dateLabel": cells[1],
            "baseCity": cells[2], "theme": cells[3], "core": cells[4],
            "option": cells[5], "fatigue": cells[6], "lock": cells[7],
        })
    return rows


def build_inventory():
    rows = parse_master()
    if [r["day"] for r in rows] != list(range(1, 44)):
        raise SystemExit("Master itinerary must contain exactly Day 1–43")
    if set(DAY_REFS) != set(range(1, 44)):
        raise SystemExit("Curated day references must cover exactly Day 1–43")

    all_sources = [str(MASTER.relative_to(ROOT)), str(AUDIT.relative_to(ROOT))]
    days = []
    identities = {}
    for row in rows:
        refs = DAY_REFS[row["day"]]
        rendered = []
        for place_id, status in refs:
            if place_id not in PLACES:
                raise SystemExit(f"Day {row['day']}: unknown place id {place_id}")
            place = PLACES[place_id]
            if status not in {"confirmed", "optional", "reference", "accommodation", "private"}:
                raise SystemExit(f"Day {row['day']}: invalid status {status}")
            if place.visibility == "private" and (status != "private" or place.photo_needed):
                raise SystemExit(f"Day {row['day']}: private place exposure risk {place_id}")
            identity = (place.name, place.name_ko, place.place_type, place.chapter)
            if place_id in identities and identities[place_id] != identity:
                raise SystemExit(f"inconsistent place identity: {place_id}")
            identities[place_id] = identity
            sources = all_sources + [REGIONAL[place.chapter]]
            rendered.append({
                "id": place_id,
                "name": place.name,
                "nameKo": place.name_ko,
                "type": place.place_type,
                "status": status,
                "importance": place.importance,
                "chapter": place.chapter,
                "visibility": place.visibility,
                "photoNeeded": place.photo_needed,
                "sourceFiles": sources,
            })
        days.append({**row, "sourceFiles": all_sources, "places": rendered})

    return {
        "schemaVersion": "1.0",
        "generatedAt": "2026-08-05",
        "travelPeriod": {"start": "2026-08-29", "end": "2026-10-10", "days": 43},
        "sourceOfTruth": str(MASTER.relative_to(ROOT)),
        "auditSources": [str(AUDIT.relative_to(ROOT)), *REGIONAL.values()],
        "privacyRule": "Private accommodation has no address, coordinates, public photo or exterior.",
        "days": days,
    }


def write_outputs(payload, base_csv: Path | None = None, day_range: tuple[int, int] | None = None):
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["date", "day", "baseCity", "theme", "id", "name", "nameKo", "type",
              "status", "importance", "chapter", "visibility", "photoNeeded", "sourceFiles"]
    base_rows = None
    if base_csv and day_range:
        # --base-csv may be the output path itself; read it before truncating.
        with base_csv.open(encoding="utf-8-sig", newline="") as base_stream:
            base_rows = list(csv.DictReader(base_stream))
    with OUTPUT_CSV.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        generated = {}
        for day in payload["days"]:
            generated[day["day"]] = []
            for place in day["places"]:
                generated[day["day"]].append({
                    "date": day["date"], "day": day["day"], "baseCity": day["baseCity"],
                    "theme": day["theme"], **{k: place[k] for k in fields[4:-1]},
                    "sourceFiles": ";".join(place["sourceFiles"]),
                })
        if base_rows is not None and day_range:
            start, end = day_range
            emitted = set()
            for row in base_rows:
                day = int(row["day"])
                if start <= day <= end:
                    if day not in emitted:
                        writer.writerows(generated[day])
                        emitted.add(day)
                else:
                    writer.writerow(row)
        else:
            for day in payload["days"]:
                writer.writerows(generated[day["day"]])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base",
        type=Path,
        help="기존 inventory를 기준으로 --days 범위만 교체한다.",
    )
    parser.add_argument(
        "--days",
        help="교체할 Day 범위(예: 16-19). --base와 함께 사용한다.",
    )
    parser.add_argument(
        "--base-csv",
        type=Path,
        help="--base 사용 시 범위 밖 CSV 행을 보존할 기존 CSV.",
    )
    args = parser.parse_args()
    payload = build_inventory()
    if args.base or args.days:
        if not (args.base and args.base_csv and args.days and re.fullmatch(r"\d+-\d+", args.days)):
            raise SystemExit("--base, --base-csv, --days START-END를 함께 지정해야 한다")
        start, end = map(int, args.days.split("-"))
        base = json.loads(args.base.read_text(encoding="utf-8"))
        replacements = {d["day"]: d for d in payload["days"] if start <= d["day"] <= end}
        base["days"] = [replacements.get(d["day"], d) for d in base["days"]]
        payload = base
    selected = tuple(map(int, args.days.split("-"))) if args.days else None
    write_outputs(payload, args.base_csv, selected)
    rows = [p for d in payload["days"] for p in d["places"]]
    unique = {p["id"] for p in rows}
    photo = {p["id"] for p in rows if p["photoNeeded"] and p["visibility"] == "public"}
    print(f"itinerary inventory: 43 days · {len(rows)} day-place rows · "
          f"{len(unique)} unique places · {len(photo)} photo-needed places")


if __name__ == "__main__":
    main()
