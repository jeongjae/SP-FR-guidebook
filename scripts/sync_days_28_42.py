import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAILY_CARDS = ROOT / 'data' / 'daily-cards'

HOTEL_PARIS = {
    'name': '78 Rue de Lourmel (파리 15구)',
    'lat': 48.8472,
    'lng': 2.2894,
    'status': 'confirmed',
    'address': '78 Rue de Lourmel, 75015 Paris, Île-de-France, France'
}

def update_day_28():
    p = DAILY_CARDS / 'day-28.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '파리 시티투어 풀 루프 & 그랑 팔레 세잔 특별전'
    d['startTime'] = '08:00'
    d['endTime'] = '21:00'
    d['totalDuration'] = '13시간'
    d['totalDistance'] = '시티투어 버스 약 15km + 메트로/도보 약 4km'
    d['fatigue'] = '3'
    d['transport'] = [
        'Tootbus / Big Bus 파리 시티투어 버스 (2층 파노라마 풀 루프 2시간 15분)',
        '메트로 8호선 (Lourmel ↔ Concorde/Champs-Élysées)'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '08:00',
            'end': '12:45',
            'name': 'Standard Home Morning (아침·운동·장보기·점심)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '08:00 숙소 아침식사 ➔ 09:00 러닝/운동 ➔ 10:15 샤워·세탁·생활용품 점검 ➔ 11:30 숙소 가벼운 점심 식사',
            'menu': '바게트, 치즈, 샐러드, 에스프레소',
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'city-bus-tour',
            'order': 2,
            'start': '13:45',
            'end': '16:15',
            'name': 'Paris City Tour Bus (파리 전역 파노라마 오리엔테이션)',
            'category': 'sight',
            'lat': 48.8661,
            'lng': 2.3125,
            'summary': '그랑 팔레 승차 ➔ 에펠탑·트로카데로 ➔ 샹젤리제·개선문 ➔ 오페라 ➔ 루브르 ➔ 노트르담 ➔ 오르세 ➔ 콩코르드 ➔ 그랑 팔레 복귀 (2시간 15분 풀 루프). 하차 없이 2주간 누빌 파리 전체 도시축 파악',
            'menu': None,
            'reservation': 'Tootbus / Big Bus Discover 티켓 사전 예매',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'grand-palais-cezanne',
            'order': 3,
            'start': '16:30',
            'end': '19:15',
            'name': 'Grand Palais — 특별전 <Cézanne et nous>',
            'category': 'culture',
            'lat': 48.8661,
            'lng': 2.3125,
            'summary': '1900년 만국박람회 유리 돔 네이브(Nef) 건축 관람 및 특별전 <Cézanne et nous> 관람. Aix 세잔 여정이 20세기 모더니즘(피카소/마티스)으로 연결되는 서사 (2시간 45분)',
            'menu': None,
            'reservation': '사전 시간지정 예약 필수 (17:00 슬롯)',
            'optional': False,
            'place_ref': 'grand-palais'
        },
        {
            'id': 'paris-return',
            'order': 4,
            'start': '19:45',
            'end': '21:00',
            'name': '15구 숙소 귀환 & 동네 저녁 식사',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '메트로 8호선으로 15구 귀환. Rue du Commerce 인근 비스트로 저녁 식사 후 휴식',
            'menu': '오리 가슴살 스테이크, 하우스 와인',
            'reservation': '현장 선택',
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'city-bus-tour',
            'mode': 'metro',
            'duration': '메트로 8호선 약 25분',
            'distance': '4.5km'
        },
        {
            'from': 'city-bus-tour',
            'to': 'grand-palais-cezanne',
            'mode': 'walk',
            'duration': '2분',
            'distance': '0.1km'
        },
        {
            'from': 'grand-palais-cezanne',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 8호선 약 25분',
            'distance': '4.5km'
        }
    ]
    d['backup'] = '우천 시 시티투어 버스 1층 실내석을 이용하고 그랑 팔레 내부 관람 및 카페 체류 시간 확대'
    d['needsReview'] = [
        'Tootbus / Big Bus 9/25 운행시간표 및 그랑 팔레 정류장 위치 확인',
        'Grand Palais Cézanne et nous 17:00 슬롯 사전 예매'
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 28')

def update_day_29():
    p = DAILY_CARDS / 'day-29.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '뤽상부르 워홀전 & 생제르맹 지성 산책 & 노트르담'
    d['startTime'] = '08:00'
    d['endTime'] = '21:00'
    d['totalDuration'] = '13시간'
    d['totalDistance'] = '메트로 + 도보 약 5.5km'
    d['fatigue'] = '3'
    d['transport'] = [
        '메트로 10호선 (La Motte-Picquet ➔ Mabillon/Odéon)',
        '파리 좌안(Left Bank) 역사문화 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '08:00',
            'end': '12:30',
            'name': 'Standard Home Morning (아침·운동·정리·점심)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '숙소 생활 루틴: 아침 러닝, 세탁, 가벼운 숙소식 점심',
            'menu': '크루아상, 그릭요거트, 샐러드',
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'luxembourg-warhol',
            'order': 2,
            'start': '13:00',
            'end': '14:30',
            'name': 'Musée du Luxembourg — 특별전 <Andy Warhol>',
            'category': 'culture',
            'lat': 48.8481,
            'lng': 2.3344,
            'summary': '프랑스 최초의 공공 미술관에서 열리는 앤디 워홀 특별전 <La ligne et l'image> 집중 관람 (90분)',
            'menu': None,
            'reservation': '사전 시간지정 예약 필수 (13:00 슬롯)',
            'optional': False,
            'place_ref': 'musee-du-luxembourg'
        },
        {
            'id': 'jardin-luxembourg',
            'order': 3,
            'start': '14:30',
            'end': '15:45',
            'name': 'Jardin du Luxembourg & 메디시스 분수',
            'category': 'sight',
            'lat': 48.8462,
            'lng': 2.3372,
            'summary': '마리 드 메디시스 궁전 정원, 17세기 그늘진 메디시스 분수대, 플라타너스 가로수길 산책 (75분)',
            'menu': 'Mademoiselle Angelina 쇼콜라 쇼, 에스프레소',
            'reservation': None,
            'optional': False,
            'place_ref': 'latin-quarter'
        },
        {
            'id': 'saint-germain',
            'order': 4,
            'start': '15:45',
            'end': '17:15',
            'name': 'Saint-Germain-des-Prés 지성미 도보',
            'category': 'sight',
            'lat': 48.8539,
            'lng': 2.3333,
            'summary': '파리에서 가장 오래된 생제르맹데프레 성당, 카페 드 플로르 & 레 뒤 마고 외관, 생쉴피스 광장 분수대 산책 (90분)',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': 'latin-quarter'
        },
        {
            'id': 'notre-dame-compact',
            'order': 5,
            'start': '17:30',
            'end': '18:45',
            'name': 'Notre-Dame de Paris & 시테 섬 (컴팩트 외관 조망)',
            'category': 'sight',
            'lat': 48.8530,
            'lng': 2.3499,
            'summary': '센 강변을 건너 시테 섬 진입. 복원된 노트르담 대성당 서쪽 파사드 및 센 강변 일몰 조망 (75분)',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': 'notre-dame-de-paris'
        },
        {
            'id': 'paris-return',
            'order': 6,
            'start': '19:15',
            'end': '21:00',
            'name': '15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '메트로 10호선으로 15구 복귀. 숙소 인근 식당 저녁 식사',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'luxembourg-warhol',
            'mode': 'metro',
            'duration': '메트로 10호선 약 20분',
            'distance': '3.8km'
        },
        {
            'from': 'luxembourg-warhol',
            'to': 'jardin-luxembourg',
            'mode': 'walk',
            'duration': '3분',
            'distance': '0.1km'
        },
        {
            'from': 'jardin-luxembourg',
            'to': 'saint-germain',
            'mode': 'walk',
            'duration': '8분',
            'distance': '0.5km'
        },
        {
            'from': 'saint-germain',
            'to': 'notre-dame-compact',
            'mode': 'walk',
            'duration': '12분',
            'distance': '0.9km'
        },
        {
            'from': 'notre-dame-compact',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 10호선 약 25분',
            'distance': '4.8km'
        }
    ]
    d['backup'] = '피로 시 노트르담 외관을 생략하고 생제르맹 카페에서 휴식 후 15구 조기 복귀'
    d['needsReview'] = ['Musée du Luxembourg 13:00 슬롯 예매 확인']
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 29')

def update_day_30():
    p = DAILY_CARDS / 'day-30.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '오랑주리 수련 연작 & 튀일르리·팔레 루아얄 고전 파리'
    d['startTime'] = '08:00'
    d['endTime'] = '21:00'
    d['totalDuration'] = '13시간'
    d['totalDistance'] = '메트로 + 도보 약 5.0km'
    d['fatigue'] = '3'
    d['transport'] = [
        '메트로 8호선 (Lourmel ↔ Concorde)',
        '파리 우안 고전 예술·정원 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '08:00',
            'end': '12:45',
            'name': 'Standard Home Morning (아침·운동·장보기·점심)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '숙소 일상 루틴 및 점심 식사',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'orangerie',
            'order': 2,
            'start': '13:30',
            'end': '15:15',
            'name': "Musée de l'Orangerie (오랑주리 미술관)",
            'category': 'culture',
            'lat': 48.8638,
            'lng': 2.3225,
            'summary': '모네의 기념비적 <수련(Nymphéas)> 타원형 자연채광 전시실 2개실 집중 감상 + 발터-기욤 컬렉션(세잔, 르누아르, 마티스, 모딜리아니) (1시간 45분)',
            'menu': None,
            'reservation': '사전 시간지정 예약 필수 (13:30 슬롯)',
            'optional': False,
            'place_ref': 'musee-de-l-orangerie'
        },
        {
            'id': 'tuileries-vendome',
            'order': 3,
            'start': '15:15',
            'end': '16:15',
            'name': 'Jardin des Tuileries & Place Vendôme',
            'category': 'sight',
            'lat': 48.8635,
            'lng': 2.3275,
            'summary': '튀일르리 정원의 대형 팔각 분수대와 조각 산책 ➔ 방돔 광장(Place Vendôme) 나폴레옹 전승기념탑 조망 (60분)',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'palais-royal',
            'order': 4,
            'start': '16:15',
            'end': '17:30',
            'name': 'Palais Royal (팔레 루아얄 안뜰 & 정원)',
            'category': 'sight',
            'lat': 48.8648,
            'lng': 2.3364,
            'summary': '다니엘 뷔랑(Daniel Buren)의 줄무늬 원통 기둥(Les Deux Plateaux) 설치미술과 고즈넉한 아케이드 회랑 정원 산책 (75분)',
            'menu': 'Café Kitsuné 에스프레소',
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'opera-garnier-district',
            'order': 5,
            'start': '17:30',
            'end': '18:30',
            'name': 'Opéra Garnier 지구 외관 산책',
            'category': 'sight',
            'lat': 48.8719,
            'lng': 2.3316,
            'summary': '샤를 가르니에의 화려한 네오바로크 파사드 조망 및 오페라 광장 산책 (60분)',
            'menu': None,
            'reservation': '내부 입장 선택(옵션)',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'paris-return',
            'order': 6,
            'start': '19:00',
            'end': '21:00',
            'name': '15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '메트로 8호선(Opéra ➔ Lourmel)으로 귀환 후 저녁 식사',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'orangerie',
            'mode': 'metro',
            'duration': '메트로 8호선 약 20분',
            'distance': '4.2km'
        },
        {
            'from': 'orangerie',
            'to': 'tuileries-vendome',
            'mode': 'walk',
            'duration': '5분',
            'distance': '0.3km'
        },
        {
            'from': 'tuileries-vendome',
            'to': 'palais-royal',
            'mode': 'walk',
            'duration': '8분',
            'distance': '0.6km'
        },
        {
            'from': 'palais-royal',
            'to': 'opera-garnier-district',
            'mode': 'walk',
            'duration': '10분',
            'distance': '0.8km'
        },
        {
            'from': 'opera-garnier-district',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 8호선 약 25분',
            'distance': '5.0km'
        }
    ]
    d['backup'] = '우천 시 야외 정원 도보를 축소하고 갤러리 비비엔(Galerie Vivienne) 등 인근 파사주(Passages) 실내 산책으로 전환'
    d['needsReview'] = ['Musée de l'Orangerie 13:30 슬롯 예매 필수 (화요일 휴관이므로 일요일 방문 엄수)']
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 30')

def update_day_31():
    p = DAILY_CARDS / 'day-31.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '모로 아틀리에 & 파리 패션위크 개막 & 마레 지구'
    d['startTime'] = '08:00'
    d['endTime'] = '20:30'
    d['totalDuration'] = '12시간 30분'
    d['totalDistance'] = '메트로 + 도보 약 6.0km'
    d['fatigue'] = '3'
    d['transport'] = [
        '메트로 12호선 / 8호선 (15구 ↔ 9구 / 마레)',
        '누벨 아테네 및 마레 지구 패션 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '08:00',
            'end': '09:45',
            'name': 'Shortened Home Morning (아침·빠른 준비)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '오전 모로 미술관 관람을 위해 아침식사 후 09:45 빠른 출발',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'gustave-moreau',
            'order': 2,
            'start': '10:30',
            'end': '12:00',
            'name': 'Musée Gustave Moreau (귀스타브 모로 미술관)',
            'category': 'culture',
            'lat': 48.8778,
            'lng': 2.3364,
            'summary': '19세기 상징주의 화가의 아틀리에 저택. 전설적인 나선형 계단, 주피터와 세멜레, 신화적 대작 유화 및 회전식 데생 패널 집중 관람 (90분)',
            'menu': None,
            'reservation': '사전 시간지정 예약 권장 (10:30 슬롯)',
            'optional': False,
            'place_ref': 'musee-gustave-moreau'
        },
        {
            'id': 'opera-lunch',
            'order': 3,
            'start': '12:15',
            'end': '13:30',
            'name': '9구 누벨 아테네 / 오페라 점심',
            'category': 'food',
            'lat': 48.8750,
            'lng': 2.3350,
            'summary': '오페라 인근 정통 프렌치 비스트로 점심 식사',
            'menu': '오늘의 요리(Plat du jour), 에스프레소',
            'reservation': '현장 선택',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'fashion-week-marais',
            'order': 4,
            'start': '14:00',
            'end': '17:30',
            'name': 'Paris Fashion Week 개막 분위기 & Le Marais',
            'category': 'sight',
            'lat': 48.8589,
            'lng': 2.3589,
            'summary': '2026 파리 패션위크(SS27 여성복) 개막일. 마레 지구의 트렌디한 거리(Rue Vieille du Temple, Rue des Francs-Bourgeois) 팝업 스토어, 쇼윈도, 부티크 거리 산책 (3.5시간)',
            'menu': '스페셜티 커피, 페이스트리',
            'reservation': None,
            'optional': False,
            'place_ref': 'le-marais'
        },
        {
            'id': 'paris-return',
            'order': 5,
            'start': '18:15',
            'end': '20:30',
            'name': '15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '메트로 8호선(Saint-Paul/Chemin Vert ➔ Lourmel) 귀환 후 15구 저녁',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'gustave-moreau',
            'mode': 'metro',
            'duration': '메트로 8+12호선 약 30분',
            'distance': '5.8km'
        },
        {
            'from': 'gustave-moreau',
            'to': 'opera-lunch',
            'mode': 'walk',
            'duration': '5분',
            'distance': '0.3km'
        },
        {
            'from': 'opera-lunch',
            'to': 'fashion-week-marais',
            'mode': 'metro',
            'duration': '메트로 약 15분',
            'distance': '2.5km'
        },
        {
            'from': 'fashion-week-marais',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 8호선 약 25분',
            'distance': '5.5km'
        }
    ]
    d['backup'] = '피로 시 마레 지구 쇼핑 도보를 90분으로 단축하고 피카소 미술관 인근 카페 휴식으로 전환'
    d['needsReview'] = [
        'Musée Gustave Moreau 화요일 휴관이므로 월요일(9/28) 10:30 슬롯 방문 엄수',
        'Fashion Week 공개 팝업 및 거리 분위기 확인 (비공개 쇼 입장 전제 없음)'
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 31')

def update_day_32():
    p = DAILY_CARDS / 'day-32.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '오르세 미술관 집중 관람 & 로댕 조각 정원'
    d['startTime'] = '07:30'
    d['endTime'] = '20:30'
    d['totalDuration'] = '13시간'
    d['totalDistance'] = '메트로 + 7구 예술도보 약 5.0km'
    d['fatigue'] = '4'
    d['transport'] = [
        '메트로 8호선 / 12호선 (Lourmel ➔ Solférino)',
        '파리 7구 오르세·로댕 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '07:30',
            'end': '08:45',
            'name': 'Art-Heavy Morning (빠른 아침·오르세 출발)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '오르세 미술관 09:30 개장 첫 슬롯 입장을 위해 아침식사 후 08:45 출발',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'musee-d-orsay',
            'order': 2,
            'start': '09:30',
            'end': '13:00',
            'name': "Musée d'Orsay (오르세 미술관 3.5시간 집중 관람)",
            'category': 'culture',
            'lat': 48.8600,
            'lng': 2.3266,
            'summary': '옛 기차역 보자르 건축. 5층 인상주의 갤러리(마네 <풀밭 위의 점심식사>, 르누아르 <물랭 드 라 갈레트의 무도회>, 모네 <양산 쓴 여인>) ➔ 2층 후기인상주의(고흐 <자화상>, <아를의 별이 빛나는 밤>, 고갱, 쇠라) ➔ 0층 초기 아카데미즘 (3.5시간)',
            'menu': None,
            'reservation': '사전 시간지정 예약 필수 (09:30 슬롯)',
            'optional': False,
            'place_ref': 'musee-d-orsay'
        },
        {
            'id': 'rue-du-bac-lunch',
            'order': 3,
            'start': '13:00',
            'end': '14:15',
            'name': '7구 Rue du Bac 점심 식사',
            'category': 'food',
            'lat': 48.8570,
            'lng': 2.3250,
            'summary': '오르세 미술관 인근 7구 품격 있는 비스트로 점심',
            'menu': '타르틴, 뵈프 부르기뇽, 화이트 와인',
            'reservation': '현장 선택',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'musee-rodin',
            'order': 4,
            'start': '14:30',
            'end': '16:30',
            'name': 'Musée Rodin & 조각 정원 (로댕 미술관)',
            'category': 'culture',
            'lat': 48.8553,
            'lng': 2.3158,
            'summary': '18세기 오텔 비롱 저택 <키스>, 카미유 클로델 전시실 ➔ 야외 장미 정원 <생각하는 사람>, <지옥의 문>, <칼레의 시민> 사색 산책 (2시간)',
            'menu': None,
            'reservation': '사전 시간지정 예약 권장 (14:30 슬롯)',
            'optional': False,
            'place_ref': 'musee-rodin'
        },
        {
            'id': 'invalides-exterior',
            'order': 5,
            'start': '16:30',
            'end': '17:30',
            'name': 'Les Invalides (앵발리드 황금 돔 외관 산책)',
            'category': 'sight',
            'lat': 48.8566,
            'lng': 2.3125,
            'summary': '나폴레옹의 무덤이 있는 앵발리드 황금 돔과 에스플러나드 잔디광장 산책 (60분)',
            'menu': None,
            'reservation': None,
            'optional': True,
            'place_ref': None
        },
        {
            'id': 'paris-return',
            'order': 6,
            'start': '18:00',
            'end': '20:30',
            'name': '15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '메트로 8호선(La Tour-Maubourg ➔ Lourmel) 귀환 후 15구 저녁',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'musee-d-orsay',
            'mode': 'metro',
            'duration': '메트로 8+12호선 약 20분',
            'distance': '3.8km'
        },
        {
            'from': 'musee-d-orsay',
            'to': 'rue-du-bac-lunch',
            'mode': 'walk',
            'duration': '5분',
            'distance': '0.3km'
        },
        {
            'from': 'rue-du-bac-lunch',
            'to': 'musee-rodin',
            'mode': 'walk',
            'duration': '8분',
            'distance': '0.6km'
        },
        {
            'from': 'musee-rodin',
            'to': 'invalides-exterior',
            'mode': 'walk',
            'duration': '5분',
            'distance': '0.4km'
        },
        {
            'from': 'invalides-exterior',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 8호선 약 20분',
            'distance': '3.5km'
        }
    ]
    d['backup'] = '오르세 관람 후 피로 시 앵발리드 산책을 생략하고 로댕 미술관 카페 정원에서 휴식 후 조기 복귀'
    d['needsReview'] = ["Musée d'Orsay 09:30 슬롯 예매 필수 (월요일 휴관이므로 화요일 9/29 방문)"]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 32')

def update_day_33():
    p = DAILY_CARDS / 'day-33.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '프티 팔레 & 몽테뉴 패션위크 & 팔레 드 도쿄'
    d['startTime'] = '08:00'
    d['endTime'] = '20:30'
    d['totalDuration'] = '12시간 30분'
    d['totalDistance'] = '메트로 + 서부 파리 도보 약 5.5km'
    d['fatigue'] = '3'
    d['transport'] = [
        '메트로 8호선 / 9호선 (15구 ↔ 샹젤리제/알마)',
        '몽테뉴 대로 및 센 강변 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '08:00',
            'end': '09:15',
            'name': 'Shortened Home Morning (아침·빠른 준비)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '프티 팔레 10:00 관람을 위해 아침식사 후 09:15 출발',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'petit-palais',
            'order': 2,
            'start': '10:00',
            'end': '12:00',
            'name': 'Petit Palais (프티 팔레 파리 시립미술관)',
            'category': 'culture',
            'lat': 48.8661,
            'lng': 2.3144,
            'summary': '1900년 만국박람회 보자르 궁전. 렘브란트 자화상, 쿠르베 <잠>, 모네 유화 무료 상설전 ➔ 아름다운 반원형 안뜰 정원 산책 (2시간)',
            'menu': None,
            'reservation': '상설전 무료 자유 입장',
            'optional': False,
            'place_ref': 'petit-palais'
        },
        {
            'id': 'champs-elysees-lunch',
            'order': 3,
            'start': '12:15',
            'end': '13:30',
            'name': '샹젤리제 인근 비스트로 점심',
            'category': 'food',
            'lat': 48.8680,
            'lng': 2.3100,
            'summary': '프티 팔레 인근 테라스 레스토랑 점심',
            'menu': '클럽 샌드위치, 니스와즈 샐러드, 에스프레소',
            'reservation': '현장 선택',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'fashion-week-montaigne',
            'order': 4,
            'start': '13:30',
            'end': '17:30',
            'name': 'Paris Fashion Week 서부 축 & Palais de Tokyo',
            'category': 'sight',
            'lat': 48.8647,
            'lng': 2.3025,
            'summary': 'Avenue Montaigne 명품 플래그십 쇼윈도 ➔ Grand Palais 일대 패션 피플 분위기 ➔ Palais de Tokyo / SPHERE 공공 컨텍스트 ➔ 센 강변 Alma 인도교 도보 산책 (4시간)',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': 'grand-palais'
        },
        {
            'id': 'paris-return',
            'order': 5,
            'start': '18:00',
            'end': '20:30',
            'name': '15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '메트로 9호선(Alma-Marceau) ➔ 15구 귀환 후 저녁',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'petit-palais',
            'mode': 'metro',
            'duration': '메트로 8+1호선 약 25분',
            'distance': '4.5km'
        },
        {
            'from': 'petit-palais',
            'to': 'champs-elysees-lunch',
            'mode': 'walk',
            'duration': '5분',
            'distance': '0.3km'
        },
        {
            'from': 'champs-elysees-lunch',
            'to': 'fashion-week-montaigne',
            'mode': 'walk',
            'duration': '8분',
            'distance': '0.5km'
        },
        {
            'from': 'fashion-week-montaigne',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 9+8호선 약 20분',
            'distance': '3.5km'
        }
    ]
    d['backup'] = '비 올 경우 팔레 드 도쿄 실내 전시 관람 및 프티 팔레 가든 카페 체류 연장'
    d['needsReview'] = ['9/30 Fashion Week 서부 Paris 축(Avenue Montaigne~Palais de Tokyo) 동선 확인']
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 33')

def update_day_34():
    p = DAILY_CARDS / 'day-34.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '베르사유 궁전 & 대정원 & 트리아농 전일 투어'
    d['startTime'] = '08:30'
    d['endTime'] = '19:30'
    d['totalDuration'] = '11시간'
    d['totalDistance'] = 'RER C 왕복 약 35km + 베르사유 영지 도보 약 7km'
    d['fatigue'] = '4'
    d['transport'] = [
        'RER C선 (Javel역 ↔ Versailles Château Rive Gauche역, 직통 25분)',
        '베르사유 광활한 영지 도보 (궁전 ➔ 정원 ➔ 대운하 ➔ 트리아농)'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'versailles-transfer',
            'order': 1,
            'start': '08:30',
            'end': '09:30',
            'name': '15구 숙소 출발 ➔ RER C ➔ 베르사유 이동',
            'category': 'transport',
            'lat': 48.8000,
            'lng': 2.1286,
            'summary': '15구 숙소에서 RER C선 Javel역 탑승 (직통 25분, 09:15 베르사유역 도착 후 궁전 도보 10분)',
            'menu': None,
            'reservation': 'RER C 티켓 / 나비고',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'versailles-palace',
            'order': 2,
            'start': '09:45',
            'end': '12:30',
            'name': 'Château de Versailles (베르사유 궁전 본관)',
            'category': 'culture',
            'lat': 48.8048,
            'lng': 2.1203,
            'summary': '10:00 시간지정 입장. 거울의 방(Galerie des Glaces 73m 거울 회랑), 국왕의 대침실, 왕실 예배당 집중 관람 (2시간 45분)',
            'menu': None,
            'reservation': 'Passport 티켓 사전 시간지정 예약 필수 (10:00 슬롯)',
            'optional': False,
            'place_ref': 'versailles'
        },
        {
            'id': 'versailles-lunch',
            'order': 3,
            'start': '12:30',
            'end': '14:00',
            'name': '베르사유 대운하 인근 점심 식사',
            'category': 'food',
            'lat': 48.8100,
            'lng': 2.1100,
            'summary': '대운하(Grand Canal) 입구 레스토랑 La Flottille에서 점심 식사 및 휴식',
            'menu': '크레프, 키슈 로렌, 시드르(사과주)',
            'reservation': '현장 선택',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'versailles-gardens',
            'order': 4,
            'start': '14:00',
            'end': '15:30',
            'name': '베르사유 프랑스식 대정원 & 분수 산책',
            'category': 'sight',
            'lat': 48.8060,
            'lng': 2.1150,
            'summary': '앙드레 르 노트르가 설계한 기하학적 프랑스 정원, 라톤의 분수, 아폴론의 분수 산책 (90분)',
            'menu': None,
            'reservation': 'Passport 티켓 포함',
            'optional': False,
            'place_ref': 'versailles'
        },
        {
            'id': 'trianon-hamlet',
            'order': 5,
            'start': '15:30',
            'end': '17:00',
            'name': 'Grand Trianon & Petit Trianon & 왕비의 촌락',
            'category': 'culture',
            'lat': 48.8150,
            'lng': 2.1050,
            'summary': '루이 14세의 분홍 대리석 이궁 그랑 트리아농, 마리 앙투아네트의 프티 트리아농 및 전원풍 왕비의 촌락(Hameau de la Reine) 관람 (90분)',
            'menu': None,
            'reservation': 'Passport 티켓 포함',
            'optional': False,
            'place_ref': 'versailles'
        },
        {
            'id': 'paris-return',
            'order': 6,
            'start': '17:30',
            'end': '19:30',
            'name': '베르사유 ➔ 15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': 'RER C선 탑승 ➔ 15구 Javel역 하차 후 숙소 복귀. 15구 숙소식 또는 동네 비스트로 저녁',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'versailles-transfer',
            'to': 'versailles-palace',
            'mode': 'walk',
            'duration': '10분',
            'distance': '0.8km'
        },
        {
            'from': 'versailles-palace',
            'to': 'versailles-lunch',
            'mode': 'walk',
            'duration': '12분',
            'distance': '0.9km'
        },
        {
            'from': 'versailles-lunch',
            'to': 'versailles-gardens',
            'mode': 'walk',
            'duration': '5분',
            'distance': '0.3km'
        },
        {
            'from': 'versailles-gardens',
            'to': 'trianon-hamlet',
            'mode': 'walk',
            'duration': '15분',
            'distance': '1.1km'
        },
        {
            'from': 'trianon-hamlet',
            'to': 'paris-return',
            'mode': 'train',
            'duration': '도보 20분 + RER C선 25분',
            'distance': '약 18km'
        }
    ]
    d['backup'] = '보행 피로 시 트리아농 이동 시 미니트레인(Petit Train)을 이용하고 왕비의 촌락은 외관만 보고 16:30 조기 복귀'
    d['needsReview'] = [
        '베르사유 Passport 티켓 10:00 궁전 슬롯 사전 예매 필수',
        'RER C선 평일 공사 여부 확인'
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 34')

def update_day_35():
    p = DAILY_CARDS / 'day-35.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '루브르 박물관 4시간 마스터피스 집중 관람'
    d['startTime'] = '08:00'
    d['endTime'] = '21:00'
    d['totalDuration'] = '13시간'
    d['totalDistance'] = '메트로 + 루브르 실내 도보 약 6.0km'
    d['fatigue'] = '4'
    d['transport'] = [
        '메트로 8호선 + 1호선 (Lourmel ➔ Palais Royal - Musée du Louvre)',
        '루브르 박물관 회랑 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '08:00',
            'end': '12:45',
            'name': 'Standard Home Morning (아침·운동·장보기·점심)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '오전 숙소 생활 루틴 및 여유로운 점심 식사',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'musee-du-louvre',
            'order': 2,
            'start': '14:00',
            'end': '18:00',
            'name': 'Musée du Louvre (루브르 박물관 4시간 집중 관람)',
            'category': 'culture',
            'lat': 48.8606,
            'lng': 2.3376,
            'summary': '유리 피라미드 진입 ➔ 드농관 1층 <모나리자>, <사모트라케의 니케>, 다비드 <나폴레옹 대관식>, 들라크루아 <민중을 이끄는 자유의 여신> ➔ 쉴리관 <밀로의 비너스>, 스핑크스 ➔ 리슐리외관 나폴레옹 3세 아파트 (4시간)',
            'menu': None,
            'reservation': '사전 시간지정 예약 필수 (14:00 슬롯)',
            'optional': False,
            'place_ref': 'musee-du-louvre'
        },
        {
            'id': 'cour-carree-seine',
            'order': 3,
            'start': '18:00',
            'end': '19:15',
            'name': 'Cour Carrée & 센 강변 일몰 산책',
            'category': 'sight',
            'lat': 48.8597,
            'lng': 2.3389,
            'summary': '루브르 르네상스 안뜰 쿠르 카레(Cour Carrée)를 통과하여 예술의 다리(Pont des Arts) 및 센 강변 일몰 산책 (75분)',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'paris-return',
            'order': 4,
            'start': '19:45',
            'end': '21:00',
            'name': '15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '메트로 1+8호선으로 15구 귀환 후 저녁 식사',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'musee-du-louvre',
            'mode': 'metro',
            'duration': '메트로 8+1호선 약 25분',
            'distance': '4.8km'
        },
        {
            'from': 'musee-du-louvre',
            'to': 'cour-carree-seine',
            'mode': 'walk',
            'duration': '3분',
            'distance': '0.2km'
        },
        {
            'from': 'cour-carree-seine',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 1+8호선 약 25분',
            'distance': '5.0km'
        }
    ]
    d['backup'] = '인지 피로 시 리슐리외관을 생략하고 드농관 핵심 걸작 위주 2.5시간 관람 후 카페 앙젤리나 휴식'
    d['needsReview'] = ['Musée du Louvre 14:00 슬롯 사전 예매 필수']
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 35')

def update_day_36():
    p = DAILY_CARDS / 'day-36.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '마르모탕 모네 <인상, 해돋이> & 파시 고급 지구 산책'
    d['startTime'] = '08:00'
    d['endTime'] = '20:00'
    d['totalDuration'] = '12시간'
    d['totalDistance'] = '메트로/버스 + 16구 도보 약 4.0km'
    d['fatigue'] = '2'
    d['transport'] = [
        '메트로 9호선 (La Muette역) 또는 32번 버스',
        '파리 16구 라늘라 정원 및 파시 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '08:00',
            'end': '12:45',
            'name': 'Standard Home Morning (아침·운동·장보기·점심)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '익일 10/4 개선문상 경마 축제를 대비한 여유로운 오전 일상 및 가벼운 점심',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'marmottan-monet',
            'order': 2,
            'start': '14:00',
            'end': '16:00',
            'name': 'Musée Marmottan Monet (마르모탕 모네 미술관)',
            'category': 'culture',
            'lat': 48.8592,
            'lng': 2.2672,
            'summary': '인상주의라는 이름을 탄생시킨 모네의 <인상, 해돋이(Impression, soleil levant)> 원작 및 지베르니 말년 대형 수련 컬렉션, 베르트 모리조 전시실 집중 감상 (2시간)',
            'menu': None,
            'reservation': '사전 시간지정 예매 권장 (14:00 슬롯)',
            'optional': False,
            'place_ref': 'musee-marmottan-monet'
        },
        {
            'id': 'ranelagh-passy',
            'order': 3,
            'start': '16:00',
            'end': '17:30',
            'name': 'Jardin du Ranelagh & Passy 역사지구 산책',
            'category': 'sight',
            'lat': 48.8580,
            'lng': 2.2725,
            'summary': '라늘라 정원 조각 산책 ➔ 16구 파시(Passy) 부르주아 지구, 발자크 생가 인근 고즈넉한 골목 산책 (90분)',
            'menu': '파시 제과점 마카롱, 에스프레소',
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'paris-return',
            'order': 4,
            'start': '18:00',
            'end': '20:00',
            'name': '15구 조기 귀환 & 저녁 (익일 Arc 대회 휴식)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '숙소 조기 복귀 후 편안한 저녁 식사 및 익일 경마 대회 드레스코드/티켓 점검',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'marmottan-monet',
            'mode': 'bus',
            'duration': '32번 버스 또는 메트로 9호선 약 25분',
            'distance': '3.5km'
        },
        {
            'from': 'marmottan-monet',
            'to': 'ranelagh-passy',
            'mode': 'walk',
            'duration': '5분',
            'distance': '0.3km'
        },
        {
            'from': 'ranelagh-passy',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 약 20분',
            'distance': '3.2km'
        }
    ]
    d['backup'] = '우천 시 라늘라 공원 산책을 생략하고 마르모탕 미술관 내부 컬렉션 감상 후 15구 조기 복귀'
    d['needsReview'] = ['Musée Marmottan Monet 14:00 슬롯 예매 확인']
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 36')

def update_day_37():
    p = DAILY_CARDS / 'day-37.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = "개선문상 경마 대회 (Qatar Prix de l'Arc de Triomphe)"
    d['startTime'] = '09:30'
    d['endTime'] = '20:30'
    d['totalDuration'] = '11시간'
    d['totalDistance'] = '메트로+셔틀 왕복 약 18km'
    d['fatigue'] = '4'
    d['transport'] = [
        "메트로 10호선 (Porte d'Auteuil역) + France Galop 공식 무료 셔틀버스(Navette)",
        '파리롱샹 경마장 보행'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'longchamp-transfer',
            'order': 1,
            'start': '10:30',
            'end': '11:30',
            'name': '15구 숙소 출발 ➔ 메트로/셔틀 ➔ ParisLongchamp',
            'category': 'transport',
            'lat': 48.8580,
            'lng': 2.2340,
            'summary': "10:30 출발 ➔ 메트로 10호선 Porte d'Auteuil역 ➔ 개선문상 전용 무료 셔틀버스 탑승 ➔ 11:30 파리롱샹 경마장 도착",
            'menu': None,
            'reservation': 'Qatar Prix de l'Arc 티켓 (General Admission / Grandstand)',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'prix-de-l-arc',
            'order': 2,
            'start': '11:30',
            'end': '18:00',
            'name': "Qatar Prix de l'Arc de Triomphe (개선문상 본선)",
            'category': 'sight',
            'lat': 48.8580,
            'lng': 2.2340,
            'summary': '세계 최고 권위 잔디 경마 축제. 패독(Paddock) 말 관람, 인터내셔널 푸드 트럭 빌리지 점심, 16:05 개선문상 메인 레이스(2,400m) 직관, 우승마 시상식 관람 (6.5시간)',
            'menu': '푸드빌리지 버거/샴페인, 프렌치 프라이',
            'reservation': "예약확정 Qatar Prix de l'Arc de Triomphe",
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'paris-return',
            'order': 3,
            'start': '18:30',
            'end': '20:30',
            'name': '파리롱샹 ➔ 15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '경기 종료 후 셔틀버스 + 메트로 10호선 탑승 ➔ 15구 숙소 복귀. 15구 숙소식 저녁 식사 및 휴식',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'longchamp-transfer',
            'to': 'prix-de-l-arc',
            'mode': 'bus',
            'duration': '셔틀버스 15분',
            'distance': '3.5km'
        },
        {
            'from': 'prix-de-l-arc',
            'to': 'paris-return',
            'mode': 'bus',
            'duration': '셔틀버스 + 메트로 10호선 약 40분 (인파 완충)',
            'distance': '8.5km'
        }
    ]
    d['backup'] = '퇴장 시 셔틀버스 대기열 과다 시 Porte de Passy 방향 도보 15분 후 버스/우버 이용'
    d['needsReview'] = [
        "Prix de l'Arc 10/4 메인 레이스 시간표(16:05) 및 셔틀 운행 재확인",
        '스마트 캐주얼 드레스코드 및 가방 반입 규정 준수'
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 37')

def update_day_38():
    p = DAILY_CARDS / 'day-38.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '개선문상 후 회복 & 자크마르-앙드레 & 몽소 공원'
    d['startTime'] = '09:00'
    d['endTime'] = '20:30'
    d['totalDuration'] = '11시간 30분'
    d['totalDistance'] = '메트로 + 도보 약 3.5km'
    d['fatigue'] = '2'
    d['transport'] = [
        '메트로 8호선 + 9호선 (Lourmel ➔ Miromesnil)',
        '8구 오스만·몽소 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '09:00',
            'end': '13:30',
            'name': 'Recovery Morning (느린 기상·브런치·세탁)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '경마 축제 다음 날 느린 기상, 세탁, 숙소 브런치 및 가벼운 15구 동네 산책',
            'menu': '프렌치 토스트, 커피, 과일',
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'jacquemart-andre',
            'order': 2,
            'start': '15:00',
            'end': '17:00',
            'name': 'Musée Jacquemart-André (자크마르-앙드레 미술관)',
            'category': 'culture',
            'lat': 48.8756,
            'lng': 2.3106,
            'summary': '19세기 벨 에포크 대저택, 나선형 계단과 겨울 정원, 보티첼리 <성모자상>, 티에폴로 천장 프레스코화 관람 (2시간)',
            'menu': 'Café Jacquemart-André 티 & 페이스트리',
            'reservation': '사전 시간지정 예약 권장 (15:00 슬롯)',
            'optional': False,
            'place_ref': 'musee-jacquemart-andre'
        },
        {
            'id': 'parc-monceau',
            'order': 3,
            'start': '17:00',
            'end': '18:30',
            'name': 'Parc Monceau (몽소 공원 고즈넉한 산책)',
            'category': 'sight',
            'lat': 48.8797,
            'lng': 2.3089,
            'summary': '8구 귀족적 풍경의 몽소 공원. 코린트식 고대 열주 나우마키아(Naumachia) 연못과 피라미드 조형물 산책 (90분)',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'paris-return',
            'order': 4,
            'start': '19:00',
            'end': '20:30',
            'name': '15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '메트로 9+8호선으로 15구 복귀. 15구 동네 비스트로 저녁 식사',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'jacquemart-andre',
            'mode': 'metro',
            'duration': '메트로 8+9호선 약 25분',
            'distance': '4.8km'
        },
        {
            'from': 'jacquemart-andre',
            'to': 'parc-monceau',
            'mode': 'walk',
            'duration': '6분',
            'distance': '0.4km'
        },
        {
            'from': 'parc-monceau',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 2+8호선 약 25분',
            'distance': '5.0km'
        }
    ]
    d['backup'] = '피로 시 몽소 공원 산책을 축소하고 미술관 내 카페에서 티타임 후 조기 복귀'
    d['needsReview'] = ['Musée Jacquemart-André 리노베이션 재개관 15:00 슬롯 예매 확인']
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 38')

def update_day_39():
    p = DAILY_CARDS / 'day-39.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '마레 지구 예술 더블 — 피카소 & 카르나발레 & 보주 광장'
    d['startTime'] = '08:00'
    d['endTime'] = '21:00'
    d['totalDuration'] = '13시간'
    d['totalDistance'] = '메트로 + 마레 지구 도보 약 5.0km'
    d['fatigue'] = '3'
    d['transport'] = [
        '메트로 8호선 (Lourmel ↔ Saint-Sébastien - Froissart / Saint-Paul)',
        '마레 지구 17세기 귀족 저택 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '08:00',
            'end': '12:00',
            'name': 'Standard Home Morning (아침·운동·장보기·점심)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '오전 숙소 일상 루틴 및 점심 식사',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'musee-picasso',
            'order': 2,
            'start': '13:00',
            'end': '15:00',
            'name': 'Musée Picasso Paris (국립 피카소 미술관)',
            'category': 'culture',
            'lat': 48.8597,
            'lng': 2.3622,
            'summary': '17세기 오텔 살레 저택. 청색 시대 자화상부터 입체주의, 조각 <염소>, 도예, 말년 대작까지 피카소 전 생애 컬렉션 집중 관람 (2시간)',
            'menu': None,
            'reservation': '사전 시간지정 예약 필수 (13:00 슬롯)',
            'optional': False,
            'place_ref': 'musee-picasso-paris'
        },
        {
            'id': 'marais-walk-carnavalet',
            'order': 3,
            'start': '15:00',
            'end': '15:30',
            'name': '마레 지구 골목 산책 ➔ 카르나발레 이동',
            'category': 'sight',
            'lat': 48.8580,
            'lng': 2.3600,
            'summary': '마레 지구 아름다운 귀족 저택 골목(Rue Payenne) 도보 산책 (30분)',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': 'le-marais'
        },
        {
            'id': 'musee-carnavalet',
            'order': 4,
            'start': '15:30',
            'end': '17:15',
            'name': 'Musée Carnavalet (카르나발레 파리 역사박물관)',
            'category': 'culture',
            'lat': 48.8572,
            'lng': 2.3625,
            'summary': '프랑스 대혁명 유물(바스티유 감옥 열쇠/벽돌), 마르셀 프루스트의 코르크 침실, 르네상스 저택 정원 관람 (1시간 45분)',
            'menu': None,
            'reservation': '상설전 무료 예약 (15:30 권장)',
            'optional': False,
            'place_ref': 'musee-carnavalet'
        },
        {
            'id': 'place-des-vosges',
            'order': 5,
            'start': '17:15',
            'end': '18:30',
            'name': 'Place des Vosges (보주 광장 & 아치 회랑)',
            'category': 'sight',
            'lat': 48.8556,
            'lng': 2.3656,
            'summary': '앙리 4세가 조성한 파리 최고(最古)의 계획 광장. 붉은 벽돌 저택 아케이드 회랑, 빅토르 위고 생가 외관, 중앙 분수대 산책 (75분)',
            'menu': 'Carette 마카롱 / 쇼콜라 쇼',
            'reservation': None,
            'optional': False,
            'place_ref': 'le-marais'
        },
        {
            'id': 'paris-return',
            'order': 6,
            'start': '19:00',
            'end': '21:00',
            'name': '15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '메트로 8호선(Chemin Vert ➔ Lourmel) 귀환 후 저녁 식사',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'musee-picasso',
            'mode': 'metro',
            'duration': '메트로 8호선 약 25분',
            'distance': '5.5km'
        },
        {
            'from': 'musee-picasso',
            'to': 'marais-walk-carnavalet',
            'mode': 'walk',
            'duration': '4분',
            'distance': '0.3km'
        },
        {
            'from': 'marais-walk-carnavalet',
            'to': 'musee-carnavalet',
            'mode': 'walk',
            'duration': '2분',
            'distance': '0.1km'
        },
        {
            'from': 'musee-carnavalet',
            'to': 'place-des-vosges',
            'mode': 'walk',
            'duration': '5분',
            'distance': '0.4km'
        },
        {
            'from': 'place-des-vosges',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 8호선 약 25분',
            'distance': '5.5km'
        }
    ]
    d['backup'] = '피로 시 카르나발레 관람 시간을 60분으로 압축하고 보주 광장 카페 카레트에서 티타임'
    d['needsReview'] = [
        'Musée Picasso Paris 13:00 슬롯 예매 필수 (월요일 휴관이므로 화요일 10/6 방문)',
        'Musée Carnavalet 무료 시간지정 티켓 예약'
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 39')

def update_day_40():
    p = DAILY_CARDS / 'day-40.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '부르스 드 코메르스 개막일 & 몽마르트르 포도 수확 축제'
    d['startTime'] = '08:00'
    d['endTime'] = '20:30'
    d['totalDuration'] = '12시간 30분'
    d['totalDistance'] = '메트로 + 몽마르트르 언덕 도보 약 6.0km'
    d['fatigue'] = '4'
    d['transport'] = [
        '메트로 8호선 / 1호선 / 12호선 (15구 ↔ 레 알 ↔ 몽마르트르 Abbesses)',
        '몽마르트르 언덕 돌계단 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '08:00',
            'end': '10:15',
            'name': 'Shortened Home Morning (아침·빠른 준비)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '11:00 부르스 드 코메르스 개막일 슬롯을 위해 10:15 출발',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'bourse-de-commerce',
            'order': 2,
            'start': '11:00',
            'end': '13:00',
            'name': 'Bourse de Commerce — Pinault Collection',
            'category': 'culture',
            'lat': 48.8625,
            'lng': 2.3425,
            'summary': '옛 곡물거래소 로툰다에 안도 타다오가 설계한 원형 콘크리트 실린더 건축 ➔ 신규 기획전 <Remember Me> 개막일 특별 관람 (2시간)',
            'menu': None,
            'reservation': '사전 시간지정 예매 필수 (10/7 개막일 11:00 슬롯)',
            'optional': False,
            'place_ref': 'bourse-de-commerce-pinault-collection'
        },
        {
            'id': 'halles-lunch',
            'order': 3,
            'start': '13:00',
            'end': '14:15',
            'name': '레 알 / 몽토르게이 점심 식사',
            'category': 'food',
            'lat': 48.8640,
            'lng': 2.3460,
            'summary': '보행자 전용 미식 거리 Rue Montorgueil 비스트로 점심',
            'menu': '스테이크 타르타르, 프렌치 오니언 수프, 로컬 와인',
            'reservation': '현장 선택',
            'optional': False,
            'place_ref': 'montorgueil'
        },
        {
            'id': 'vendanges-montmartre',
            'order': 4,
            'start': '14:45',
            'end': '17:45',
            'name': 'Fête des Vendanges de Montmartre (포도축제 & 몽마르트르)',
            'category': 'sight',
            'lat': 48.8867,
            'lng': 2.3431,
            'summary': '메트로 12호선 Abbesses역 도착 ➔ 몽마르트르 포도원(Clos Montmartre) 외관 축제 분위기 ➔ 라팽 아질 ➔ 테르트르 광장 ➔ 사크레쾨르 대성당 파리 전경 (3시간)',
            'menu': '축제 길거리 음식, 몽마르트르 와인',
            'reservation': None,
            'optional': False,
            'place_ref': 'montmartre-south-pigalle'
        },
        {
            'id': 'paris-return',
            'order': 5,
            'start': '18:15',
            'end': '20:30',
            'name': '15구 숙소 귀환 & 저녁',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '메트로 12+8호선으로 15구 귀환 후 편안한 저녁',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'bourse-de-commerce',
            'mode': 'metro',
            'duration': '메트로 8+1호선 약 25분',
            'distance': '4.8km'
        },
        {
            'from': 'bourse-de-commerce',
            'to': 'halles-lunch',
            'mode': 'walk',
            'duration': '5분',
            'distance': '0.4km'
        },
        {
            'from': 'halles-lunch',
            'to': 'vendanges-montmartre',
            'mode': 'metro',
            'duration': '메트로 4+12호선 약 20분',
            'distance': '3.5km'
        },
        {
            'from': 'vendanges-montmartre',
            'to': 'paris-return',
            'mode': 'metro',
            'duration': '메트로 12+8호선 약 30분',
            'distance': '6.8km'
        }
    ]
    d['backup'] = '우천 또는 인파 과다 시 몽마르트르 포도원 외관 산책만 컴팩트하게 진행하고 사크레쾨르 내부 관람 후 조기 복귀'
    d['needsReview'] = [
        'Bourse de Commerce 10/7 신규 기획전 <Remember Me> 개막일 11:00 슬롯 예매',
        'Vendanges de Montmartre 10/7(수) 공식 행사 일정 확인 (주말 퍼레이드와 혼동 금지)'
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 40')

def update_day_41():
    p = DAILY_CARDS / 'day-41.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '기메 동양미술관 & 파리 현대미술관 & 트로카데로 고별 일몰'
    d['startTime'] = '08:00'
    d['endTime'] = '21:30'
    d['totalDuration'] = '13시간 30분'
    d['totalDistance'] = '메트로 + 서부 파리 예술도보 약 5.0km'
    d['fatigue'] = '3'
    d['transport'] = [
        '메트로 9호선 / 6호선 (15구 ↔ Iéna / Trocadéro)',
        '이에나 광장 및 트로카데로 도보'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'morning-routine',
            'order': 1,
            'start': '08:00',
            'end': '09:15',
            'name': 'Art-Heavy Morning (빠른 아침·기메 출발)',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '마지막 Full Day. 10:00 기메 박물관 입장을 위해 아침식사 후 09:15 출발',
            'menu': None,
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'musee-guimet',
            'order': 2,
            'start': '10:00',
            'end': '12:00',
            'name': 'Musée Guimet (국립 기메 동양박물관)',
            'category': 'culture',
            'lat': 48.8650,
            'lng': 2.2936,
            'summary': '간다라 헬레니즘 불상, 앙코르와트 크메르 조각 걸작, 시바 나타라자 청동상, 한국실 삼국시대 불상 및 달항아리 관람 (2시간)',
            'menu': None,
            'reservation': '사전 시간지정 예약 권장 (10:00 슬롯)',
            'optional': False,
            'place_ref': 'musee-guimet'
        },
        {
            'id': 'iena-lunch',
            'order': 3,
            'start': '12:00',
            'end': '13:15',
            'name': '이에나 / 윌슨 대로변 점심 식사',
            'category': 'food',
            'lat': 48.8645,
            'lng': 2.2960,
            'summary': '기메 박물관과 현대미술관 사이 프레지던트 윌슨 대로 테라스 점심',
            'menu': '파리지앵 샐러드, 파스타, 에스프레소',
            'reservation': '현장 선택',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'musee-art-moderne',
            'order': 4,
            'start': '13:30',
            'end': '15:45',
            'name': "Musée d'Art Moderne de Paris (MAM)",
            'category': 'culture',
            'lat': 48.8647,
            'lng': 2.2978,
            'summary': '팔레 드 도쿄 동관. 라울 뒤피의 600㎡ 세계 최대 유화 벽화 <전기의 요정>, 앙리 마티스 <댄스>, 2026 뒤샹상(Prix Marcel Duchamp) 특별전 관람 (2시간 15분)',
            'menu': None,
            'reservation': '상설전 무료 자유 입장',
            'optional': False,
            'place_ref': 'musee-d-art-moderne-de-paris'
        },
        {
            'id': 'trocadero-sunset',
            'order': 5,
            'start': '16:00',
            'end': '18:30',
            'name': 'Place du Trocadéro ➔ 에펠탑 고별 일몰 조망',
            'category': 'sight',
            'lat': 48.8625,
            'lng': 2.2875,
            'summary': '트로카데로 광장 에스플러나드에서 에펠탑 정면 파노라마 조망 ➔ 이에나 다리 건너 에펠탑 아래 샹드마르스 공원 일몰 산책 (2.5시간)',
            'menu': '샴페인/로컬 와인 글라스',
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'farewell-dinner',
            'order': 6,
            'start': '19:00',
            'end': '21:30',
            'name': '파리 15박 마무리 고별 만찬 (Farewell Dinner) & 숙소 귀환',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '15구/7구 엄선 프렌치 비스트로에서 43일 유럽 여행을 마무리하는 고별 저녁 만찬 후 숙소 복귀. 익일 출국 짐 패킹',
            'menu': '프렌치 정통 코스 디너 (에스카르고, 스테이크, 수플레, 보르도 와인)',
            'reservation': '저녁 예약 필수',
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'morning-routine',
            'to': 'musee-guimet',
            'mode': 'metro',
            'duration': '메트로 9호선 약 20분',
            'distance': '3.5km'
        },
        {
            'from': 'musee-guimet',
            'to': 'iena-lunch',
            'mode': 'walk',
            'duration': '3분',
            'distance': '0.2km'
        },
        {
            'from': 'iena-lunch',
            'to': 'musee-art-moderne',
            'mode': 'walk',
            'duration': '4분',
            'distance': '0.3km'
        },
        {
            'from': 'musee-art-moderne',
            'to': 'trocadero-sunset',
            'mode': 'walk',
            'duration': '8분',
            'distance': '0.6km'
        },
        {
            'from': 'trocadero-sunset',
            'to': 'farewell-dinner',
            'mode': 'metro',
            'duration': '메트로 6호선 약 15분',
            'distance': '2.5km'
        }
    ]
    d['backup'] = '우천 시 트로카데로 야외 산책을 단축하고 샤이오 궁 인근 카페에서 에펠탑 뷰 감상'
    d['needsReview'] = [
        'Musée Guimet 10:00 슬롯 예매 (화요일 휴관이므로 목요일 10/8 방문)',
        '고별 저녁 식당 예약 확정'
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 41')

def update_day_42():
    p = DAILY_CARDS / 'day-42.json'
    d = json.loads(p.read_text(encoding='utf-8'))
    d['title'] = '파리 15박 체크아웃 ➔ CDG 공항 ➔ 인천 귀국 (OZ502)'
    d['startTime'] = '08:00'
    d['endTime'] = '19:10'
    d['totalDuration'] = '11시간 10분'
    d['totalDistance'] = '택시/RER 약 35km + 비행'
    d['fatigue'] = '3'
    d['transport'] = [
        '파리 공식 택시 (15구 ➔ CDG 터미널 1 정액제 약 60분, €65)',
        '아시아나항공 OZ502 (CDG 19:10 ➔ ICN 10/10 14:10, 확정)'
    ]
    d['hotel'] = HOTEL_PARIS
    d['stops'] = [
        {
            'id': 'paris-packing-checkout',
            'order': 1,
            'start': '08:00',
            'end': '11:00',
            'name': '15구 숙소 최종 짐 정리 & 체크아웃',
            'category': 'hotel',
            'lat': 48.8472,
            'lng': 2.2894,
            'summary': '15박 장기 체류 짐 최종 패킹, 분리수거 및 숙소 점검. 11:00 정식 체크아웃',
            'menu': None,
            'reservation': '체크아웃 11:00',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'farewell-lunch',
            'order': 2,
            'start': '11:30',
            'end': '13:00',
            'name': '15구 생활권 마지막 점심 식사',
            'category': 'food',
            'lat': 48.8468,
            'lng': 2.2905,
            'summary': '단골 15구 비스트로/카페에서 파리 생활을 회고하는 마지막 점심 식사',
            'menu': '크로크무슈, 샐러드, 에스프레소',
            'reservation': None,
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'cdg-transfer',
            'order': 3,
            'start': '13:30',
            'end': '15:00',
            'name': '15구 숙소 ➔ CDG 공항 터미널 1 이동',
            'category': 'transport',
            'lat': 49.0097,
            'lng': 2.5479,
            'summary': '13:30 공식 택시 탑승(파리 우안/좌안 정액 요금 €65, 약 60~75분 소요). 15:00 CDG 터미널 1 여유롭게 도착 (출발 4시간 전 도착으로 교통체증/수속 리스크 완전 차단)',
            'menu': None,
            'reservation': '공식 택시 G7 또는 호텔 콜택시',
            'optional': False,
            'place_ref': None
        },
        {
            'id': 'cdg-departure',
            'order': 4,
            'start': '15:00',
            'end': '19:10',
            'name': 'CDG 공항 출국 수속 & OZ502 탑승',
            'category': 'transport',
            'lat': 49.0097,
            'lng': 2.5479,
            'summary': '아시아나 카운터 수하물 위탁 ➔ PABLO 전자 택스리펀 ➔ 보안검색 및 출국심사 ➔ 면세점/라운지 휴식 ➔ 19:10 OZ502 탑승',
            'menu': None,
            'reservation': '예약확정 아시아나항공 OZ502 (CDG 19:10 ➔ ICN 10/10 14:10)',
            'optional': False,
            'place_ref': None
        }
    ]
    d['legs'] = [
        {
            'from': 'paris-packing-checkout',
            'to': 'farewell-lunch',
            'mode': 'walk',
            'duration': '5분',
            'distance': '0.3km'
        },
        {
            'from': 'farewell-lunch',
            'to': 'cdg-transfer',
            'mode': 'taxi',
            'duration': '택시 약 75분 (교통 완충 포함)',
            'distance': '35.0km'
        },
        {
            'from': 'cdg-transfer',
            'to': 'cdg-departure',
            'mode': 'walk',
            'duration': '공항 내 이동',
            'distance': '0.5km'
        }
    ]
    d['backup'] = '고속도로 정체 시 13:00 조기 출발하여 15:00 이전 공항 도착 완수'
    d['needsReview'] = [
        'CDG 터미널 1 택스리펀(PABLO 바코드 스캔) 준비',
        '아시아나 OZ502 19:10 탑승권 및 수하물 태그 확인'
    ]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "
", encoding='utf-8')
    print('Updated Day 42')

if __name__ == '__main__':
    update_day_28()
    update_day_29()
    update_day_30()
    update_day_31()
    update_day_32()
    update_day_33()
    update_day_34()
    update_day_35()
    update_day_36()
    update_day_37()
    update_day_38()
    update_day_39()
    update_day_40()
    update_day_41()
    update_day_42()
