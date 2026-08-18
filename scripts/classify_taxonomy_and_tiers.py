#!/usr/bin/env python3
"""PC-01 Taxonomy Normalization & PC-02 Priority / Content Tier Classification

Generates:
- PLACE_TAXONOMY_NORMALIZATION.md
- PLACE_CONTENT_TIER_MAP.md
- PLACE_TAXONOMY_AND_TIERS.csv
"""
import csv
import json
import os
import re
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parent.parent

# 104 Canonical Places with Normalized Taxonomy, Priority, and Content Tier
PLACE_CLASSIFICATIONS = {
    # BARCELONA (10)
    "sagrada-familia": {
        "norm_type": "architecture",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "가우디의 대표작, 바르셀로나 핵심 랜드마크, 심화 건축/예술 해설 필수"
    },
    "sant-pau-recinte-modernista": {
        "norm_type": "architecture",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "도메네크 이 몬타네르의 모더니즘 걸작 병원, 필수 관람지"
    },
    "barri-gotic": {
        "norm_type": "neighborhood",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "로마시대~중세 역사 지구, 도보 동선 및 심화 가이드 필수"
    },
    "macba": {
        "norm_type": "museum",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "라발 지구의 현대미술관 및 광장 스케이터 문화 중심지"
    },
    "biblioteca-de-catalunya": {
        "norm_type": "historic_site",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "구 산타 크레우 병원 부지, 고딕 양식 중정과 역사 도서관"
    },
    "cau-ferrat": {
        "norm_type": "museum",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "시체스 루시뇰 아틀리에 미술관, 카탈루냐 모더니즘 핵심 컬렉션"
    },
    "palau-de-maricel": {
        "norm_type": "architecture",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "시체스 해안가 복합 궁전, 지중해 뷰와 예술 컬렉션"
    },
    "sitges": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "바르셀로나 근교 예술가 해변 마을, Day 3 반일 투어 거점"
    },
    "barcelona-sants": {
        "norm_type": "transit",
        "priority": "WORTHWHILE",
        "content_tier": "UTILITY",
        "rationale": "TGV/AVE 철도 관문 및 이동 노드 (유틸리티/환승 가이드)"
    },
    "barcelona-historic-walk": {
        "norm_type": "walk",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "고딕~보른~해변으로 이어지는 역사 도보 코스"
    },
    "barcelona-modernisme-walk": {
        "norm_type": "walk",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "에이샴플레 모더니즘 건축군 탐방 도보 코스"
    },

    # GIRONA & COSTA BRAVA (9)
    "girona-cathedral": {
        "norm_type": "architecture",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "단일 신랑 세계 최대 폭 고딕 성당, 지로나 랜드마크"
    },
    "passeig-de-la-muralla": {
        "norm_type": "viewpoint",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "지로나 중세 성벽길, 구시가지와 피레네 조망 뷰포인트"
    },
    "onyar": {
        "norm_type": "viewpoint",
        "priority": "MUST_SEE",
        "content_tier": "TIER_B",
        "rationale": "오냐르 강변 파사드와 에펠 다리 조망 포인트"
    },
    "pals": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "엠포르다 지역의 보존된 중세 석조 마을"
    },
    "peratallada": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "바위 해자 성곽과 미로 골목이 살아있는 중세 마을"
    },
    "calella-de-palafrugell": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "코스타 브라바의 전통 어촌 해변 마을 및 카미 데 론다"
    },
    "collioure": {
        "norm_type": "village",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "야수파 마티스의 고향, 프랑스 국경 해안 요새 마을"
    },
    "peralada": {
        "norm_type": "village",
        "priority": "OPTIONAL",
        "content_tier": "TIER_C",
        "rationale": "카스텔 페랄라다 성과 와인 카르멘 와이너리 마을"
    },
    "girona-old-town-walk": {
        "norm_type": "walk",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "유대인 지구(El Call)와 중세 골목 도보 탐방"
    },

    # NICE & CÔTE D'AZUR (15)
    "promenade-des-anglais": {
        "norm_type": "viewpoint",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "니스 해변의 상징적 7km 산책로 및 지중해 조망"
    },
    "vieux-nice": {
        "norm_type": "neighborhood",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "니스 구시가지의 바로크 성당, 골목길, 로컬 문화"
    },
    "cours-saleya": {
        "norm_type": "market",
        "priority": "MUST_SEE",
        "content_tier": "UTILITY",
        "rationale": "구시가지 꽃시장·청과시장·먹거리 마켓"
    },
    "colline-du-chateau": {
        "norm_type": "viewpoint",
        "priority": "MUST_SEE",
        "content_tier": "TIER_B",
        "rationale": "천사의 만과 니스 구시가지 최고의 파노라마 전망 언덕"
    },
    "marche-de-la-liberation": {
        "norm_type": "market",
        "priority": "WORTHWHILE",
        "content_tier": "UTILITY",
        "rationale": "현지 주민 중심의 니스 최대 로컬 식료품 시장"
    },
    "saint-paul-de-vence": {
        "norm_type": "village",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "샤갈의 안식처, 성벽으로 둘러싸인 중세 예술가 마을"
    },
    "grasse": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "세계 향수의 수도, 프라고나르 향수 공방과 역사 지구"
    },
    "cannes": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "영화제의 도시, 크루아제트 해변과 르 쉬케 언덕"
    },
    "le-suquet": {
        "norm_type": "neighborhood",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "칸 구시가지 언덕, 성채 박물관과 칸 만 전망"
    },
    "marche-forville": {
        "norm_type": "market",
        "priority": "WORTHWHILE",
        "content_tier": "UTILITY",
        "rationale": "칸 최고의 프로방스 상설 시장"
    },
    "monaco": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "모나코 공국, 르 로셰와 몬테카를로"
    },
    "le-rocher": {
        "norm_type": "historic_site",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "모나코 대공궁과 구시가지가 위치한 바위 언덕 요새"
    },
    "nice-walk": {
        "norm_type": "walk",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "마세나 광장~구시가지~살레야~성 언덕 도보 코스"
    },
    "cannes-walk": {
        "norm_type": "walk",
        "priority": "OPTIONAL",
        "content_tier": "TIER_C",
        "rationale": "칸 크루아제트~르 쉬케 도보 코스"
    },
    "monaco-walk": {
        "norm_type": "walk",
        "priority": "OPTIONAL",
        "content_tier": "TIER_C",
        "rationale": "헤라클레스 항구~대공궁~몬테카를로 도보 코스"
    },
    "nce-t2": {
        "norm_type": "transit",
        "priority": "WORTHWHILE",
        "content_tier": "UTILITY",
        "rationale": "니스 코트다쥐르 공항 T2 환승 노드"
    },
    "nice-ville": {
        "norm_type": "transit",
        "priority": "WORTHWHILE",
        "content_tier": "UTILITY",
        "rationale": "니스 빌 중앙 철도역 노드"
    },

    # AIX-EN-PROVENCE (12)
    "cours-mirabeau": {
        "norm_type": "neighborhood",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "플라타너스 가로수와 분수대가 늘어선 엑스의 중심 거리"
    },
    "rotonde": {
        "norm_type": "viewpoint",
        "priority": "MUST_SEE",
        "content_tier": "TIER_B",
        "rationale": "로통드 분수대, 엑스 구시가지 진입 관문"
    },
    "place-richelme-place-des-precheurs": {
        "norm_type": "market",
        "priority": "MUST_SEE",
        "content_tier": "UTILITY",
        "rationale": "플라타너스 그늘 아래 열리는 일일 청과·프로방스 시장"
    },
    "atelier-des-lauves": {
        "norm_type": "museum",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "폴 세잔의 마지막 아틀리에, 유품과 아틀리에 정원"
    },
    "bastide-du-jas-de-bouffan": {
        "norm_type": "historic_site",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "세잔 가문의 저택 및 초기 작품 배경지"
    },
    "carrieres-de-bibemus": {
        "norm_type": "historic_site",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "붉은 사암 채석장, 세잔 입체주의적 시각의 탄생지"
    },
    "montagne-sainte-victoire-terrain-des-peintres": {
        "norm_type": "viewpoint",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "생트 빅투아르 산을 조망하는 세잔의 야외 화판 언덕"
    },
    "musee-granet": {
        "norm_type": "museum",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "엑스 대표 미술관, 세잔 및 인상파/현대 회화 컬렉션"
    },
    "cassis": {
        "norm_type": "village",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "파스텔톤 항구와 백와인, 칼랑크 국립공원의 거점 마을"
    },
    "calanques": {
        "norm_type": "nature",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "지중해 석회암 피오르드 해안 국립공원 (보트/하이킹)"
    },
    "marseille": {
        "norm_type": "neighborhood",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "프랑스 제2의 항구도시, 복합 문화와 지중해 관문"
    },
    "vieux-port-marseille": {
        "norm_type": "viewpoint",
        "priority": "MUST_SEE",
        "content_tier": "TIER_B",
        "rationale": "마르세유 구항구, 아침 어시장 및 포스터 거울 차양"
    },
    "mucem": {
        "norm_type": "museum",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "유럽·지중해 문명 박물관, 루디 리치오티의 레이스 콘크리트 건축"
    },
    "fort-saint-jean": {
        "norm_type": "historic_site",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "17세기 항구 요새 및 구름다리 보행로"
    },
    "le-panier": {
        "norm_type": "neighborhood",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "마르세유 최고(最古)의 언덕 골목 지구, 예술 공방과 벽화"
    },
    "notre-dame-de-la-garde": {
        "norm_type": "architecture",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "마르세유 최고봉 언덕 성당, 황금 성모상과 지중해 전경"
    },

    # LUBERON (11)
    "gordes": {
        "norm_type": "village",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "뤼베롱을 대표하는 절벽 위 석조 요새 마을"
    },
    "village-des-bories": {
        "norm_type": "historic_site",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "모르타르 없이 돌을 쌓아 올린 프로방스 고대 건식 석조 주거지"
    },
    "abbaye-de-senanque": {
        "norm_type": "architecture",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "계곡 속 12세기 시토회 수도원과 라벤더 밭"
    },
    "roussillon-sentier-des-ocres": {
        "norm_type": "nature",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "붉은 황토(Ochre) 절벽과 소나무 숲 산책로"
    },
    "menerbes": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "피터 메일의 소설 배경지, 고즈넉한 성채 마을"
    },
    "bonnieux": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "뤼베롱 계곡을 마주보는 계단식 언덕 마을"
    },
    "lourmarin": {
        "norm_type": "village",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "알베르 카뮈의 영면지, 르네상스 성과 금요 시장의 세련된 마을"
    },
    "goult": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "관광객이 적고 풍차가 있는 조용한 뤼베롱 숨은 보석 마을"
    },
    "oppede-le-vieux": {
        "norm_type": "historic_site",
        "priority": "OPTIONAL",
        "content_tier": "TIER_C",
        "rationale": "중세 유적과 폐허가 숲속에 남아있는 신비로운 옛 마을"
    },
    "l-isle-sur-la-sorgue": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "소르그 강의 물레방아와 프랑스 최대 앤틱 시장의 도시"
    },
    "coustellet": {
        "norm_type": "market",
        "priority": "WORTHWHILE",
        "content_tier": "UTILITY",
        "rationale": "뤼베롱 일요 농민 직거래 시장 거점"
    },

    # AVIGNON & ALPILLES (16)
    "palais-des-papes": {
        "norm_type": "architecture",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "14세기 아비뇽 유수의 교황청 요새 궁전"
    },
    "pont-saint-benezet": {
        "norm_type": "historic_site",
        "priority": "MUST_SEE",
        "content_tier": "TIER_B",
        "rationale": "론 강의 아비뇽 다리 유적과 역사"
    },
    "rocher-des-doms": {
        "norm_type": "viewpoint",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "교황청 옆 언덕 정원, 론 강과 빌뇌브레자비뇽 조망"
    },
    "saint-remy-de-provence": {
        "norm_type": "village",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "노스트라다무스의 탄생지, 알피유 산맥 기슭의 프로방스 소도시"
    },
    "glanum": {
        "norm_type": "historic_site",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "갈로-로마 시대 고대 도시 유적 및 개선문/묘탑"
    },
    "saint-paul-de-mausole": {
        "norm_type": "historic_site",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "반 고흐가 <별이 빛나는 밤>을 그린 수도원 정신병원"
    },
    "les-baux-de-provence": {
        "norm_type": "historic_site",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "석회암 바위산 위 중세 요새 성채 마을"
    },
    "carrieres-des-lumieres": {
        "norm_type": "museum",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "거대 채석장 동굴 벽면의 몰입형 미디어 아트 전시"
    },
    "arles": {
        "norm_type": "village",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "고흐의 도시이자 로마 유적 유네스코 세계유산 도시"
    },
    "arenes-d-arles": {
        "norm_type": "historic_site",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "기원전 1세기 로마 원형 투기장"
    },
    "theatre-antique-arles": {
        "norm_type": "historic_site",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "고대 로마 극장 유적과 아를의 비너스 발굴지"
    },
    "cloitre-saint-trophime": {
        "norm_type": "architecture",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "로마네스크/고딕 양식의 생 트로핌 성당 중정 회랑"
    },
    "place-du-forum-arles": {
        "norm_type": "viewpoint",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "고흐 <밤의 카페 테라스> 배경 광장"
    },
    "fondation-vincent-van-gogh-arles": {
        "norm_type": "museum",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "반 고흐의 예술적 유산과 현대미술 기획전"
    },
    "la-roquette": {
        "norm_type": "neighborhood",
        "priority": "OPTIONAL",
        "content_tier": "TIER_C",
        "rationale": "아를 론 강변의 옛 어부 지구 및 현지인 주거 골목"
    },
    "pont-du-gard": {
        "norm_type": "historic_site",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "세계 최고의 보존도를 자랑하는 3단 로마 수도교 유네스코 유산"
    },
    "uzes": {
        "norm_type": "village",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "프랑스 제1의 공작 도시, 에르브 광장 시장과 토요 마켓"
    },

    # LYON (7)
    "fourviere": {
        "norm_type": "architecture",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "푸르비에르 언덕 노트르담 바실리카 및 리옹 시내 조망"
    },
    "vieux-lyon": {
        "norm_type": "neighborhood",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "르네상스 건축 지구, 비밀 통로 트라불(Traboules), 부숑"
    },
    "croix-rousse": {
        "norm_type": "neighborhood",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "견직공(Canuts)의 역사 언덕, 벽화, 공방과 계단길"
    },
    "bellecour": {
        "norm_type": "viewpoint",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "프랑스 최대 규모의 보행자 광장, 루이 14세 기마상과 생텍쥐페리 동상"
    },
    "halles-de-lyon-paul-bocuse": {
        "norm_type": "market",
        "priority": "MUST_SEE",
        "content_tier": "UTILITY",
        "rationale": "미식의 수도 리옹의 미식 상설 홀, 최고급 식재료와 부숑"
    },
    "parc-de-la-tete-d-or": {
        "norm_type": "nature",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "황금머리 호수 공원, 식물원, 온실과 장미원"
    },
    "annecy": {
        "norm_type": "village",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "알프스의 베니스, 안시 호수와 팔레 드 릴 중세 운하 마을"
    },

    # PARIS (24)
    "musee-du-louvre": {
        "norm_type": "museum",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "세계 최대 박물관, 모나리자·밀로의 비너스·사모트라케의 니케"
    },
    "musee-d-orsay": {
        "norm_type": "museum",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "구 기차역을 개조한 19세기 인상파·후기인상파의 성지"
    },
    "musee-de-l-orangerie": {
        "norm_type": "museum",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "모네의 거대한 <수련> 연작 타원형 전용 전시실"
    },
    "centre-pompidou": {
        "norm_type": "museum",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "렌조 피아노의 하이테크 건축과 국립현대미술관"
    },
    "bourse-de-commerce-pinault-collection": {
        "norm_type": "museum",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "안도 타다오가 개조한 구 곡물거래소 피노 컬렉션 현대미술관"
    },
    "musee-marmottan-monet": {
        "norm_type": "museum",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "모네 <인상, 해돋이> 원작을 소장한 저택 미술관"
    },
    "grand-palais": {
        "norm_type": "architecture",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "1900년 만국박람회 유리 돔 궁전 및 기획전"
    },
    "bnf-richelieu": {
        "norm_type": "architecture",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "프랑스 국립도서관 라브루스트 열람실(Salle Labrouste)과 마자랭 갤러리"
    },
    "notre-dame-de-paris": {
        "norm_type": "architecture",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "시테 섬의 고딕 걸작, 2024년 재개관 대성당"
    },
    "le-marais": {
        "norm_type": "neighborhood",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "보주 광장, 귀족 저택 오텔 파르티퀼리에, 부티크와 갤러리"
    },
    "latin-quarter": {
        "norm_type": "neighborhood",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "소르본 대학, 팡테옹, 룩셈부르크 공원과 서점 거리"
    },
    "montmartre-south-pigalle": {
        "norm_type": "neighborhood",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "사크레쾨르, 테르트르 광장, 예술가 거점과 피갈 카페거리"
    },
    "montorgueil": {
        "norm_type": "neighborhood",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "파리에서 가장 오래된 보행자 미식 보행자 거리 (스토레 등)"
    },
    "les-halles": {
        "norm_type": "neighborhood",
        "priority": "WORTHWHILE",
        "content_tier": "TIER_B",
        "rationale": "파리의 심장, 카노페 건축과 생퇴스타슈 성당"
    },
    "versailles": {
        "norm_type": "architecture",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "루이 14세의 절대왕정 궁전, 거울의 방과 정원, 트리아농"
    },
    "giverny": {
        "norm_type": "historic_site",
        "priority": "MUST_SEE",
        "content_tier": "TIER_A",
        "rationale": "클로드 모네의 집과 수련 연못 정원"
    }
}

def run_pc01_pc02():
    # Load canonical places from CSV
    csv_in = ROOT / "PLACE_MASTER_INVENTORY.csv"
    canonical_rows = []
    with open(csv_in, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r["source_status"] != "DAY_CARD_STOP_ONLY":
                canonical_rows.append(r)

    print(f"Loaded {len(canonical_rows)} canonical places from inventory.")

    enriched_records = []
    for r in canonical_rows:
        slug = r["id"]
        cls_info = PLACE_CLASSIFICATIONS.get(slug, {
            "norm_type": r["current_type"],
            "priority": "WORTHWHILE",
            "content_tier": "TIER_B",
            "rationale": "기본 분류 배정"
        })
        enriched_records.append({
            "id": slug,
            "name": r["name"],
            "region": r["region"],
            "legacy_type": r["current_type"],
            "normalized_type": cls_info["norm_type"],
            "priority": cls_info["priority"],
            "content_tier": cls_info["content_tier"],
            "day_refs": r["day_refs"],
            "has_dedicated_place_page": r["has_dedicated_place_page"],
            "current_content_depth": r["current_content_depth"],
            "rationale": cls_info["rationale"]
        })

    # 1. Output PLACE_TAXONOMY_AND_TIERS.csv
    csv_out = ROOT / "PLACE_TAXONOMY_AND_TIERS.csv"
    fieldnames = [
        "id", "name", "region", "legacy_type", "normalized_type",
        "priority", "content_tier", "day_refs", "has_dedicated_place_page",
        "current_content_depth", "rationale"
    ]
    with open(csv_out, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in enriched_records:
            writer.writerow(row)
    print(f"Wrote {csv_out}")

    # Stats
    type_counts = Counter(r["normalized_type"] for r in enriched_records)
    tier_counts = Counter(r["content_tier"] for r in enriched_records)
    prio_counts = Counter(r["priority"] for r in enriched_records)
    region_counts = Counter(r["region"] for r in enriched_records)

    # 2. Output PLACE_TAXONOMY_NORMALIZATION.md (PC-01)
    tax_md = ROOT / "PLACE_TAXONOMY_NORMALIZATION.md"
    tax_lines = [
        "# PLACE TAXONOMY NORMALIZATION REPORT (Phase PC-01)",
        "",
        "**작성일**: 2026-08-18",
        "**대상**: 104개 Canonical Places 및 Day Stops 정규화",
        "",
        "## 1. 정규화 Taxonomy 체계 정의",
        "",
        "기존의 단순 `spot` 위주(101개) 분류에서 여행자 관점의 명확한 목적별 9대 표준 Taxonomy로 정규화하였습니다.",
        "",
        "| Normalized Type | 설명 | 수량 | 대표 장소 |",
        "|---|---|---|---|",
        f"| `architecture` | 역사적 기념비, 성당, 궁전 등 핵심 건축물 | {type_counts['architecture']}개 | 사그라다 파밀리아, 교황청, 베르사유 |",
        f"| `museum` | 미술관, 박물관, 갤러리 | {type_counts['museum']}개 | 루브르, 오르세, 세잔 아틀리에, MUCEM |",
        f"| `historic_site` | 유적지, 원형경기장, 수도원 등 | {type_counts['historic_site']}개 | 퐁뒤가르, 아를 원형경기장, 세낭크 |",
        f"| `neighborhood` | 역사 지구, 주요 거리, 구시가지 구역 | {type_counts['neighborhood']}개 | 고딕지구, 비외니스, 르마레, 비외리옹 |",
        f"| `village` | 근교 소도시, 거점 마을 | {type_counts['village']}개 | 시체스, 생폴드방스, 고르드, 아를, 안시 |",
        f"| `market` | 상설 홀, 야외 마켓, 식료품 시장 | {type_counts['market']}개 | 살레야 마켓, 리옹 폴보퀴즈 홀, 리셸름 광장 |",
        f"| `viewpoint` | 전망대, 파노라마 뷰 포인트, 주요 광장 | {type_counts['viewpoint']}개 | 니스 성 언덕, 마르세유 구항구, 벨쿠르 광장 |",
        f"| `nature` | 국립공원, 피오르드 해안, 자연 명소 | {type_counts['nature']}개 | 칼랑크 국립공원, 루시용 황토길, 테트도르 공원 |",
        f"| `walk` | 선별된 테마 도보/산책 코스 | {type_counts['walk']}개 | 바르셀로나 고딕 도보, 니스 해안 도보 |",
        f"| `transit` | 공항, 주요 철도역 노드 (유틸리티) | {type_counts['transit']}개 | 산츠역, 니스빌역, 니스공항 T2 |",
        "",
        "## 2. 기존 Type vs 정규화 Type 비교",
        "",
        "| 기존 Type (Legacy) | 수량 | → 정규화 Type (Normalized) | 수량 |",
        "|---|---|---|---|",
        f"| `spot` | 101개 | `architecture`, `museum`, `historic_site`, `neighborhood`, `village`, `market`, `viewpoint`, `nature` | {104 - type_counts['walk'] - type_counts['transit']}개 |",
        f"| `walk` | 2개 | `walk` | {type_counts['walk']}개 |",
        f"| `node` | 1개 | `transit` | {type_counts['transit']}개 |",
        "",
        "## 3. Day Stops 중 Place Taxonomy 편입 권장 맛집/카페",
        "",
        "43일 일정표(`data/daily-cards/`)의 231개 정차점 중 향후 독립 장소로 승격을 권장하는 핵심 미식 거점:",
        "- **바르셀로나**: Bar Cañete (`bar-canete`), Bodega Joan (`bodega-joan`), La Paradeta (`la-paradeta-sagrada`)",
        "- **니스/코트다쥐르**: Chez Pipo (소카 명가), René Socca, Fenocchio (아이스크림)",
        "- **엑상프로방스/뤼베롱**: Les Deux Garçons, Maison Weibel",
        "- **리옹**: Café des Fédérations (전통 부숑), Daniel & Denise",
        "- **파리**: Stohrer (가장 오래된 파티세리), Breizh Café (크레프리), Bouillon Chartier"
    ]
    with open(tax_md, "w", encoding="utf-8") as f:
        f.write("\n".join(tax_lines))
    print(f"Wrote {tax_md}")

    # 3. Output PLACE_CONTENT_TIER_MAP.md (PC-02)
    tier_md = ROOT / "PLACE_CONTENT_TIER_MAP.md"
    tier_lines = [
        "# PLACE CONTENT TIER & PRIORITY CLASSIFICATION MAP (Phase PC-02)",
        "",
        "**작성일**: 2026-08-18",
        "**총 대상**: 104개 Canonical Places",
        "",
        "## 1. Content Tier 및 Priority 요약",
        "",
        "### 1.1 Content Tier 분포",
        f"- **Tier A (Signature Place / 심화 가이드 필수)**: **{tier_counts['TIER_A']}개** ({tier_counts['TIER_A']/len(enriched_records)*100:.1f}%)",
        f"- **Tier B (Core Place / 핵심 가이드)**: **{tier_counts['TIER_B']}개** ({tier_counts['TIER_B']/len(enriched_records)*100:.1f}%)",
        f"- **Tier C (Supporting / 선택지)**: **{tier_counts['TIER_C']}개** ({tier_counts['TIER_C']/len(enriched_records)*100:.1f}%)",
        f"- **Utility (Market / Transit / 실용 허브)**: **{tier_counts['UTILITY']}개** ({tier_counts['UTILITY']/len(enriched_records)*100:.1f}%)",
        "",
        "### 1.2 Priority 분포",
        f"- **MUST_SEE (필수 방문)**: **{prio_counts['MUST_SEE']}개** ({prio_counts['MUST_SEE']/len(enriched_records)*100:.1f}%)",
        f"- **WORTHWHILE (우선 추천)**: **{prio_counts['WORTHWHILE']}개** ({prio_counts['WORTHWHILE']/len(enriched_records)*100:.1f}%)",
        f"- **OPTIONAL (선택 방문)**: **{prio_counts['OPTIONAL']}개** ({prio_counts['OPTIONAL']/len(enriched_records)*100:.1f}%)",
        "",
        "## 2. Tier A (Signature Place) 목록 — 37개",
        "",
        "| ID (Slug) | 한국어 명칭 | Region | Normalized Type | 배정 사유 |",
        "|---|---|---|---|---|"
    ]
    for r in enriched_records:
        if r["content_tier"] == "TIER_A":
            tier_lines.append(f"| `{r['id']}` | {r['name']} | {r['region']} | `{r['normalized_type']}` | {r['rationale']} |")

    tier_lines.extend([
        "",
        "## 3. Tier B (Core Place) 목록 — 53개",
        "",
        "| ID (Slug) | 한국어 명칭 | Region | Normalized Type | 배정 사유 |",
        "|---|---|---|---|---|"
    ])
    for r in enriched_records:
        if r["content_tier"] == "TIER_B":
            tier_lines.append(f"| `{r['id']}` | {r['name']} | {r['region']} | `{r['normalized_type']}` | {r['rationale']} |")

    tier_lines.extend([
        "",
        "## 4. Tier C & Utility Place 목록 — 14개",
        "",
        "| ID (Slug) | 한국어 명칭 | Region | Tier | Type | 배정 사유 |",
        "|---|---|---|---|---|---|"
    ])
    for r in enriched_records:
        if r["content_tier"] in ("TIER_C", "UTILITY"):
            tier_lines.append(f"| `{r['id']}` | {r['name']} | {r['region']} | `{r['content_tier']}` | `{r['normalized_type']}` | {r['rationale']} |")

    with open(tier_md, "w", encoding="utf-8") as f:
        f.write("\n".join(tier_lines))
    print(f"Wrote {tier_md}")

if __name__ == "__main__":
    run_pc01_pc02()
